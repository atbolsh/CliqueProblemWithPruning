Attempt to make a reasonably fast discrete clique-searcher. 
It's still exponential in runtime, definitely.

The main principle is to find "n-strong cores" of a graph: 
a node is only kept if it has n-1 or more neighbors, and an edge
only kept if its two endpoints have n-2 or more common neighbors.
This pruning is repeated until the network doesn't shrink from further passes
(it's easy to prove that this process is deterministic and polynomial).

If an n-clique exists, it'll be a subset of the n-core. Moreover, if an 
n-core has only n elements in it, that's a clique.

These two observations significantly help prune the search tree, by finding 
the core for the large network, by finding it within local network (common 
neighbors of the endpoint of an edge, or all the neighbors of a given vertex),
and help after deleting a vertex or even a single edge (one edge gone can lead to 
a cascade effect, with a lot of pruning).

I tried both vertex-recursion and edge-recursion.

Based on existing clique literature, though, it's clear I'm not the only one 
to have thought of this kind of pruning method, so I won't spend too much more time on it.

Just a fun excursion.
