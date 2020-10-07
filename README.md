MPMP15 - Prime Pairs
========================

Simple solution for Matt Parker's MPMP15 Prime Pairs puzzle

See: http://think-maths.co.uk/primepairs

Puzzle Summary
------------------

The problem is to arrange all the positive integers in the range [1,n] such that all adjacent pairs sum to a prime.

Algorithm
------------

This program creates an undirected graph where edges are labelled 1, 2, ..., n.  Nodes v and w are connected if
is_prime(v+w) is True.

Once the graph is created we find a Hamiltonian path through the graph and output that as the solution.  Note that
the solution output will not be unique (as the reverse of the output will also be valid, plus other possible
arrangements).

Experimentally this program has output solutions for n in range [9, 700].  While this is not proof that such a
prime-pair is always possible, it suggests that it may be.

Usage
---------

To use the program simply run `python prime_pairs.py [n]`


Thanks
---------

Thanks to Dmitry Sergeev for posting his Hamiltonian Path algorithm on Stack Overflow:
https://stackoverflow.com/questions/47982604/hamiltonian-path-using-python.  I could have written that part myself,
but I was busy and lazy.  Code-sharing is always appreciated :)
