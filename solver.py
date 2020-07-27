#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

from DP import dynamic_prog
from BB import branch_and_bound
from Greedy import greedy_density

def solve_it(n_shire=10, verbose=True, greedy=False):

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
    
    if greedy:
        if verbose: print("Try greedy approach")
        value, taken = greedy_density(capacity, items)
    elif dpsize < 20e6:
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
    tmp = shires_won[:1]
    last = tmp[0]
    for s in shires_won:
        if int(s)>int(last)+1:
            if last != tmp[-1]:
                tmp[-1] += '-'+last
            tmp.append(s)
        elif s==shires_won[-1]:
            if last != tmp[-1]:
                tmp[-1] += '-'+s
            else: tmp.append(s) 
        last = s
    shires_won = tmp
    if verbose:
        print()
        print("Electoral votes won: {0} of {1} ({2:.1f}%)".format(elec_votes, elec_total, elec_perc))
        print("Popular votes won: {0} of {1} ({2:.1f}%)".format(votes, total, perc))
        if(len(shires_won)>1): print("Shires won: " + ", ".join(shires_won[:-1]) + " and " + shires_won[-1])
        else:                  print("Shires won: " + shires_won[0])

    return perc


if __name__ == '__main__':

    n_shire = 10
    verbose = True
    greedy = False
    if len(sys.argv) > 1:
        n_shire = int(sys.argv[1])
    if len(sys.argv) > 2:
        greedy = int(sys.argv[2])
        
    solve_it(n_shire, verbose, greedy)

