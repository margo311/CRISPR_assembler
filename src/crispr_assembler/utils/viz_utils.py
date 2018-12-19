import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def prepare_pos(arrs, start_x = 0, start_y = 0, shift_x = 1, shift_y = 1):
    pos = {}
    x, y = 0, 0
    for arr in arrs:
        for el in arr:
            pos[el] = (x,y)
            x += shift_x
        y += shift_y
        x = 0
    return pos, x, y

def create_shift_pos(pos, x_shift = 0, y_shift = -0.2):
    s_pos = {}
    for item in pos.items():
        s_pos[item[0]] = (item[1][0] + x_shift, item[1][1] + y_shift)
    return s_pos

def add_pos(arr, pos):
    vertexes = []
    for x in [x for y in arr for x in y]:
        if not x in pos.keys():
            vertexes.append(x)

    for i, v in enumerate(vertexes):
        pos[v] = (i % 10, -1 * (i // 10  +1))
    
    return pos

def gr_to_pairs(adj):
    pairs = []
    a, b = np.where(adj == 1)
    for p in zip(a,b):
        pairs.append((p[0], p[1]))
    return pairs


def arrays_to_gr(arrays):
    G = nx.DiGraph()
    for arr in arrays:
        G.add_path(arr)
    return G

def adj_to_gr(adj):
    G = nx.DiGraph()
    a, b = np.where(adj == 1)
    for p in zip(a,b):
        G.add_edge(p[0], p[1])
    return G


def plot_graphs(*gr, figsize=(15, 10), colors = ['r', 'g', 'y', 'b'], node_size=20):
    f = plt.figure(figsize=figsize)
    ax = f.add_subplot(111)
    for i, (graph, pos) in enumerate(zip(gr[::2], gr[1::2])):

        nx.draw_networkx(graph, node_size = node_size, node_color=colors[i], alpha = 0.7, pos=pos, ax = ax)
        
    return f
       
    