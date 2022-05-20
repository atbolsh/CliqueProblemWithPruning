import numpy as np
import math

def subnetwork_from_vertex_list(H, vs):
    """Accepts edge matrix H, and list of vertices. Returns subnetwork alone"""
    return H[vs][:, vs]

def _vertex_local_network(H, vertex):
    """Accepts edge matrix H, and index. 
    Local matrix does not include the original index, only the neighbors."""
    vertices = []
    for i in range(H.shape[0]):
        if H[vertex, i]:
            vertices.append(i) # There are 0s on the main diagonal, so the original vertex
    return subnetwork_from_vertex_list(H, vertices), vertices

def _edge_local_network(H, edge):
    """Accepts edge matrix H, and tuple of indeces.
    Local matrix does not include the original edge, only the 
    common neighbors of the vertices. Returns empty array 
    if the edge is not present in H."""
    if H[edge[0], edge[1]] == 0:
        return np.array([[]]), []
    vertices = []
    for i in range(H.shape[0]):
        if H[edge[0], i] and H[edge[1], i]:
            vertices.append(i) # There are 0s on the main diagonal, so the edge vertices will be excluded here
    return subnetwork_from_vertex_list(H, vertices), vertices

def local_network(H, obj):
    """Accepts edge matrix H, obj as an index or as a tuple of indices (edge)"""
    if type(obj) == int:
        return _vertex_local_network(H, obj)
    else:
        return _edge_local_network(H, obj)

def valid_node(H, i, n):
    """Checks that node i is valid, to order n (has n - 1 neighbors or more)"""
    return np.sum(H[i]) >= n - 1

def valid_ish_node(H, i, n):
    """Checks whether node is valid OR 0"""
    s = np.sum(H[i])
    return s >= n-1 or z == 0

def valid_edge(H, i, j, n):
    """Checks that edge i, j exists AND vertices i, j have at least n-2 common neighbors."""
    return H[i, j] and np.dot(H[i], H[j]) >= n - 2

def check_n_strong(H, n): # Can have disconnected nodes with no connections
    N = H.shape[0]
    for i in range(N):
        if not valid_ish_node(H, i, n):
            return False
        for j in range(i, N):
            if H[i, j] and (not valid_edge(H, i, j, n)):
                return False
    return True

def delete_in_place(H, delNodes, deadNodes):
    """deadNodes is array, 'True' for all nodes already dead. 
    delNodes is array, True for all nodes to delet this round."""
    N = H.shape[0]
    for i in range(N):
        if deadNodes[i]:
            continue
        elif delNodes[i]:
            H[i] = np.zeros(N)
        else:
            for j in range(N): # Compiles faster than settng columns, I think
                if delNodes[j]:
                    H[i, j] = 0
    return H

def one_step_trim(H, n, s):
    """Iterative procedure to find the n-strong core of H. S is bool array, "True" for all already deleted nodes."""
    N = H.shape[0]
    to_delete = [False for i in range(N)]
    modified = False
    for i in range(N):
        if s[i]:
            continue
        if not valid_node(H, i, n):
            to_delete[i] = True
            modified = True
    if modified:
        delete_in_place(H, to_delete, s)
        for i in range(N): # One big "dead" list
            if to_delete[i]:
                s[i] = True
    for i in range(N):
        if s[i]:
            continue
        for j in range(i, N): # Earlier ones already handled
            if H[i, j] and not valid_edge(H, i, j, n):
                H[i, j], H[j, i] = 0, 0
                modified = True
    return H, s, modified

def get_strong_core(H, n, s = None):
    """Returns the n-strong core. Modifies the matriix in-place, so be careful."""
    N = H.shape[0]
    if s is None:
        s = [False for i in range(N)] 
    modified = True
    while modified:
        H, s, modified = one_step_trim(H, n, s)
    return H, s

# Initial results: I'll definitely need to iterate into "strong-strong" cores and the like, but we'll get to that later.

def num_nodes(deadList): # True if node has been deleted from the network
    return len(deadList) - sum(deadList) 

def local2global(globalGuide, localNodes):
    return [globalGuide[node] for node in localNodes]


def get_n_clique(H, n):
    N = H.shape[0]
    if n <= 0:
        raise ValueError("Use non-zero clique size")
    if n == 1:
        return [0]
    if n == 2:
        for i in range(N):
            for j in range(N):
                if H[i, j]: # connected
                    return [i, j]
        return [] # Graph completely empty; failed to find any edge.
    # We got here means n >= 3
    s = [False for i in range(N)]
    while num_nodes(s) > 0:
        H, s = get_strong_core(H, n, s)
        if num_nodes(s) == 0:
            return []
        if num_nodes(s) == n:
            return [i for i in range(N) if (not s[i])]
        # Pick first edge. Will maybe add randomness here later.
        for i in range(N):
            for j in range(N):
                if H[i, j]:
                    break
            if H[i, j]:
                break
        # Compute local network, operations on it
        LH, vs = local_network(H, (i, j))
        Q = get_n_clique(LH, n - 2) # recurse onto local network.
        # If clique, return; else, remove edge, retry.
        if len(Q) == n - 2:
            return local2global(vs, Q) + [i, j]
        elif len(Q) == 0:
            H[i, j], H[j, i] = 0, 0 # Remove the edge, recompute core.
        else:
            raise ValueError("Invalid return size; something went wrong, go back and check")
    return [] # If we found a clique, we return from within the loop

def get_n_clique_vertex(H, n):
    N = H.shape[0]
    if n <= 0:
        raise ValueError("Use non-zero clique size")
    if n == 1:
        return [0]
    if n == 2:
        for i in range(N):
            for j in range(N):
                if H[i, j]: # connected
                    return [i, j]
        return [] # Graph completely empty; failed to find any edge.
    # We got here means n >= 3
    s = [False for i in range(N)]
    while num_nodes(s) > 0:
        H, s = get_strong_core(H, n, s)
        if num_nodes(s) == 0:
            return []
        if num_nodes(s) == n:
            return [i for i in range(N) if (not s[i])]
        # Pick first edge. Will maybe add randomness here later.
        for i in range(N):
            if not s[i]:
                break
        # Compute local network, operations on it
        LH, vs = local_network(H, i)
        Q = get_n_clique(LH, n - 1) # recurse onto local network.
        # If clique, return; else, remove edge, retry.
        if len(Q) == n - 1:
            return local2global(vs, Q) + [i]
        elif len(Q) == 0:
            H[i] = np.zeros(N) # Remove the vertex
            for j in range(N):
                H[j, i] = 0
            s[i] = True
        else:
            raise ValueError("Invalid return size; something went wrong, go back and check")
    return [] # If we found a clique, we return from within the loop


