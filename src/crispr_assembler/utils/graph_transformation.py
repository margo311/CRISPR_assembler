import numpy as np
import sys

import itertools
import matplotlib.pyplot as plt


def gr_to_pairs(gr):
    N = gr.shape[0]
    pairs = [x for x in itertools.product(range(N), range(N))]
    pairs_counts = {}
    
    for p in pairs:
        if gr[p[0], p[1]] > 0: pairs_counts[p] = gr[p[0], p[1]].astype(int)
    
    
    p_to_n = dict(zip(pairs_counts.keys(), np.arange(len(pairs)).astype(int)))
    n_to_p = dict(zip(np.arange(len(pairs)).astype(int), pairs_counts.keys()))
    
    return pairs_counts, p_to_n, n_to_p, N


def pairs_to_sparse_gr(p_to_n):
    N_gr = len(p_to_n)
    N = np.array([max(x) for x in p_to_n]).max()
    first = dict(zip(range(N + 1), [[] for i in range(N + 1)] ))
    second = dict(zip(range(N + 1), [[] for i in range(N + 1)]))
    
    #print(N, first, second)
    
    for p in p_to_n.keys():
        first[p[0]].append(p)
        second[p[1]].append(p)
    
    gr = np.zeros((N_gr, N_gr))
    
    for p in p_to_n.keys():
        for p2 in first[p[1]]:
            gr[p_to_n[p]][p_to_n[p2]] = 1
        for p2 in second[p[0]]:
            gr[p_to_n[p2]][p_to_n[p]] = 1
            
            
    return gr, first, second


def make_vertexes_embs(gr, p_to_n):
    embs = np.zeros((len(p_to_n), 5))
    
    for i, p in enumerate(sorted(p_to_n.keys())):
        embs[i, 0] = gr[p[0], p[1]]
        embs[i, 1] = embs[i, 0] / gr[p[0]].sum()
        embs[i, 2] = embs[i, 0] / gr[:, p[1]].sum()
        
        embs[i, 3] = embs[i, 0] / max(1, gr[:, p[0]].sum())
        embs[i, 4] = embs[i, 0] / max(1, gr[p[1]].sum())
    return embs
        

def make_y(gr_y, p_to_n):
    y = np.zeros(len(p_to_n)).astype(int)
    
    for i, p in enumerate(p_to_n.keys()):
        y[i] = (gr_y[p[0], p[1]] > 0).astype(int)
        
    return y


def process_graph(grx, gry):
    pairs, p_to_n, n_to_p, N = gr_to_pairs(grx)
    
    adj = pairs_to_sparse_gr(p_to_n)[0]
    
    vertex_embs = make_vertexes_embs(grx, p_to_n)
    answ = make_y(gry, p_to_n) 
    
    return adj, vertex_embs, answ, p_to_n

