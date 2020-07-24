#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

from DP import dynamic_prog
from BB import branch_and_bound

def solve_it(n_shire=10, verbose=True):

    capacity = int(n_shire * (n_shire + 5) / 2)

    if capacity%2==0: capacity = int(capacity/2 - 1)
    else:             capacity = int(capacity/2)
    
    items = []

    for i in range(n_shire):
        items.append(Item(i, 5*i + 6, i + 3))

    dpsize = capacity * n_shire
    
    if verbose:
        print()
        print("DP size = {0}M".format(dpsize/1e6))
    
    if dpsize < 20e6:
        if verbose: print("Try dynamic programming")
        value, taken = dynamic_prog(capacity, items, verbose)
    else:
        if verbose: print("Try branch and bound")
        value, taken = branch_and_bound(capacity, items, verbose)

    weight = 0

    for item in items:
        if taken[item.index]:
            weight += item.weight

    votes = int(n_shire * (7 + 5*n_shire) / 2) - value
    total = n_shire * (6 + 5*n_shire)
    perc  = 100. * votes / total
    elec_total = int(n_shire * (5 + n_shire) / 2)
    elec_votes = elec_total - weight
    elec_perc  = 100. * elec_votes / elec_total
    shires_won = []
    for item in items:
        if not taken[item.index]:
            shires_won.append("{0}".format(item.index+1))
    if verbose:
        print()
        print("Electoral votes won: {0} of {1} ({2:.1f}%)".format(elec_votes, elec_total, elec_perc))
        print("Popular votes won: {0} of {1} ({2:.1f}%)".format(votes, total, perc))
        print("Shires won: " + ", ".join(shires_won[:-1]) + " and " + shires_won[-1])

    return perc


if __name__ == '__main__':

    n_shire = 10
    if len(sys.argv) > 1:
        n_shire = int(sys.argv[1])
        
    solve_it(n_shire)

