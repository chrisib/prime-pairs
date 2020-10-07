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

def is_prime(x):
    """
    Naively check if a number is a prime by checking for divisibility by 2 & all
    odd numbers <= sqrt(x).  Not the most efficient, but simple and it works.
    """
    if x % 2 == 0:
        return False

    max = int(math.ceil(math.sqrt(x)))
    for i in range(3,max+1,2):
        if x % i == 0:
            return False

    return True

def build_graph(vertices):
    """
    Create a graph represented by adjacency lists with edges such that
    V and W are connected if (V+W) is prime
    """
    graph = {}
    for v in vertices:
        graph[v] = []

        for w in vertices:
            if v == w:
                continue

            x = v+w
            if is_prime(x):
                graph[v].append(w)
    return graph

def hamilton(graph, start_at):
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
    args = parser.parse_args()

    N = args.n
    V = range(1,N+1)
    G = build_graph(V)

    # find a path that starts with 1
    start_at = 1
    path = hamilton(G, start_at)

    # if we didn't find a path maybe we just can't start at 1
    # try the next starting point, and keep going until we've tried finding
    # a path starting at every node
    # note: in practice it appears possible to start at 1 all the time, but that's
    # just a conjecture
    while len(path) != len(V) and start_at <= V[-1]:
        start_at = start_at+1
        path = hamilton(G, start_at)

    if len(path) == len(V):
        print(path)
    else:
        print("No prime-pairs path found with the numbers [1,{0}]".format(N))
