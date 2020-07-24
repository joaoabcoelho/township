from collections import namedtuple

def get_upper_bound(capacity, items):

    value = 0
    weight = 0
    index = 0
    nitems = len(items)
    
    while weight < capacity and index < nitems:
    
        item = items[index]
    
        if capacity > weight + item.weight:
            value += item.value
            weight += item.weight
        else:
            fraction = float(capacity - weight) / item.weight
            value += fraction * item.value
            weight = capacity
        
        index+=1
            
    return value

Sol = namedtuple("Sol", ["value", "taken"])
Node = namedtuple("Node", ["value","remain","taken"])

def branch_and_bound(capacity, items, verbose=True):

    sorted_items = sorted(items, key=lambda x: -float(x.value)/x.weight)

    nitems = len(sorted_items)

    best = Sol(0, [0]*nitems)
    
    nodes = [Node(0,capacity,[])]
    
    count_nodes = 0

    while len(nodes) > 0:
    
        if count_nodes % 1000000 == 0 and count_nodes>0:
            if verbose: print("Analysed {0}M nodes".format(count_nodes/1e6))
    
        count_nodes += 1
    
        node = nodes[0]
        ntaken = len(node.taken)
        
        if ntaken == nitems:
            if node.value > best.value:
                best = Sol(node.value, node.taken)
                if verbose: print("New best solution:",best.value)
            del nodes[0]
            continue
    
        upper_bound = node.value + get_upper_bound(node.remain, sorted_items[ntaken:])
        
        if upper_bound <= best.value:
            del nodes[0]
            continue
        
        v1 = node.value
        v2 = v1 + sorted_items[ntaken].value
        
        w1 = node.remain
        w2 = w1 - sorted_items[ntaken].weight
        
        t1 = node.taken + [0]
        t2 = node.taken + [1]
        
        del nodes[0]
        
        nodes = [Node(v1, w1, t1)] + nodes

        if w2 >= 0:
            nodes = [Node(v2, w2, t2)] + nodes


    if verbose: print("{0} nodes used".format(count_nodes))
    
    taken = [0]*len(items)
    
    for i in range(nitems):
        taken[sorted_items[i].index] = best.taken[i]

    return (best.value, taken)
