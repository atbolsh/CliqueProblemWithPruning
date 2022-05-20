from copy import deepcopy
from helpers import *
from graphreader import *
import time

def almost_star(n):
    H = np.ones((n, n), dtype=int)
    for i in range(n):
        H[i, i] = 0
        j = (i + 1) % n
        H[i, j], H[j, i] = 0, 0
    return H

H = almost_star(8)

print("Testing Vertex Method\n################\n\n")

print("Small Network")
print("3-clique results:")
print(get_n_clique_vertex(deepcopy(H), 3))
print('\n\n')
print("4-clique results:")
print(get_n_clique_vertex(deepcopy(H), 4))
print('\n\n')
print("5-clique results:")
print(get_n_clique_vertex(deepcopy(H), 5))
print('\n\n')


########

H = getGraph(b200_2, N200_2)

print("b200_2")
print("10-clique results")
print(get_n_clique_vertex(deepcopy(H), 10))
print('\n\n')
print("12-clique results")
print(get_n_clique_vertex(deepcopy(H), 12))
print('\n\n')

########

H = getGraph()
print("c125_9")
start = time.time()
print("34-clique")
print(get_n_clique_vertex(deepcopy(H), 34))
print('time, hrs, for the 34-clique')
print((time.time() - start)/3600)
print('\n\n')

#########
#########

print("Testing Edge Method\n################\n\n")

print("Small Network")
print("3-clique results:")
print(get_n_clique(deepcopy(H), 3))
print('\n\n')
print("4-clique results:")
print(get_n_clique(deepcopy(H), 4))
print('\n\n')
print("5-clique results:")
print(get_n_clique(deepcopy(H), 5))
print('\n\n')


########

print("b200_2")
H = getGraph(b200_2, N200_2)
print("10-clique results")
print(get_n_clique(deepcopy(H), 10))
print('\n\n')
print("12-clique results")
print(get_n_clique(deepcopy(H), 12))
print('\n\n')

########

print("c125_9")
H = getGraph()
start = time.time()
print("34-clique")
print(get_n_clique(deepcopy(H), 34))
print('time, hrs, for the 34-clique')
print((time.time() - start)/3600)
print('\n\n')

