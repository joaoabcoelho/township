
def greedy_density(capacity, items):

    sorted_items = sorted(items, key=lambda x: float(x.value) / x.weight, reverse=True)
    #sorted_items = sorted(items, key=lambda x: float(x.weight), reverse=True)
    
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in sorted_items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return (value, taken)
