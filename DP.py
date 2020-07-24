
cache = dict()

def oracle(k, n, items):

    if n < 0 or k <= 0:
        return 0

    if (k,n) in cache:
        return cache[(k,n)]
        
    vn = items[n].value
    wn = items[n].weight

    if wn <= k:
        sol1 = items[n].value + oracle(k-wn, n-1, items)
    else:
        sol1 = 0

    sol2 = oracle(k, n-1, items)
    
    result = max(sol1, sol2)

    cache[(k,n)] = result

    return result

def dynamic_prog(capacity, items, verbose=True):

    sorted_items = sorted(items, key=lambda x: x.weight)

    value = 0
    k_remain = capacity
    
    taken = [0]*len(sorted_items)
            
    for n in range(len(items)-1, -1, -1):
        
        if oracle(k_remain, n, sorted_items) > oracle(k_remain, n-1, sorted_items):
            taken[sorted_items[n].index] = 1
            k_remain -= sorted_items[n].weight
            value += sorted_items[n].value
            #print sorted_items[n]
    
    if verbose:
        print("Cached {0} out of {1} table entries ({2:.2g}%)"
              .format(len(cache), len(items)*capacity, 
                      100*float(len(cache))/len(items)/capacity))

    return (value, taken)
