#!/usr/bin/env/python
"""
Chris I-B's solution to Matt Parker's Prime-Pairs problem:

    Given the set of integers [1,N], arrange the numbers in some permutation
    such that every pair of sequential numbers sums to a prime

We build an undirected graph with vertices [1,N] with edges connecting vertices
whose values sum to a prime, and then find a Hamiltonian path through the
resulting graph
"""

import argparse

import math;

def find_all_primes(x):
    """
    Return a list of all prime numbers up-to and including x
    """
    primes=[]

    for n in range (1,x+1):
        if is_prime(n):
            primes.append(n)
    return primes

def is_prime(x, known_primes=None):
    """
    Naively check if a number is a prime by checking for divisibility by 2 & all
    odd numbers <= sqrt(x).  Not the most efficient, but simple and it works.

    Alternatively, if known_primes is a list of ints, we check if x is in that list
    and don't do any divisibility checks.  This is faster, but requires known_primes
    be complete, sorted, and cover a sufficiently large range
    """
    if known_primes == None:
        if x % 2 == 0:
            return False

        max = int(math.ceil(math.sqrt(x)))
        for i in range(3,max+1,2):
            if x % i == 0:
                return False

        return True
    else:
        return x in known_primes

def build_graph(vertices):
    """
    Create a graph represented by adjacency lists with edges such that
    V and W are connected if (V+W) is prime
    """
    graph = {}
    # calculate all known primes up to 2*the number of vertices
    # this will cover the largest possible integer we can make by summing
    # 2 numbers in the set together, making it faster to check for primality
    # as we build the graph
    known_primes = find_all_primes(2 * len(vertices))
    for v in vertices:
        graph[v] = []

        for w in vertices:
            if v == w:
                continue

            x = v+w
            if is_prime(x, known_primes):
                graph[v].append(w)
    return graph

def hamilton(graph, start_at, verbose=False):
    """
    Find and return a Hamiltonian path through a graph
    Thanks to Dmitry Sergeev via https://stackoverflow.com/questions/47982604/hamiltonian-path-using-python
    for this function, as I was too lazy to write it myself.
    """
    size = len(graph)
    # if None we are -unvisiting- comming back and pop v
    to_visit = [None, start_at]
    path = []
    while(to_visit):
        v = to_visit.pop()
        if v :
            if verbose:
                print("Visiting {0}".format(v))
                print("   Path so far: {0}".format(path))
            path.append(v)
            if len(path) == size:
                break
            for x in set(graph[v])-set(path):
                to_visit.append(None) # out
                to_visit.append(x) # in
        else: # if None we are comming back and pop v
            path.pop()
    return path

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Arrange positive numbers in the range [1,N] such that all adjacent pairs sum to a prime number')
    parser.add_argument('n', metavar='N', type=int, action='store', help='The inclusive upper limit of the range', default=9)
    parser.add_argument('-g','--print-graph', action='store_true', dest='print_graph', help='Print the graph as well as the sequence')
    parser.add_argument('-v','--verbose',action='store_true', dest='verbose', help='Enable additional output')
    args = parser.parse_args()

    if args.verbose:
        print('Building graph')

    N = args.n
    V = range(1,N+1)
    G = build_graph(V)

    if args.print_graph:
        for k in G.keys():
            print('{0}: {1}'.format(k, G[k]))

    if args.verbose:
        print('Done building graph')

    # find a path that starts with 1
    start_at = 1
    path = hamilton(G, start_at, verbose=args.verbose)

    # if we didn't find a path maybe we just can't start at 1
    # try the next starting point, and keep going until we've tried finding
    # a path starting at every node
    # note: in practice it appears possible to start at 1 all the time, but that's
    # just a conjecture
    while len(path) != len(V) and start_at <= V[-1]:
        if args.verbose:
            print('No path possible starting at {0}.  Trying again from {1}'.format(start_at, start_at+1))

        start_at = start_at+1
        path = hamilton(G, start_at)

    if len(path) == len(V):
        print(path)
    else:
        print("No prime-pairs path found with the numbers [1,{0}]".format(N))
