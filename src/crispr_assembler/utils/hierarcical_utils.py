import editdistance as ed
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from tqdm import tqdm_notebook
from collections import Counter, OrderedDict
import pickle


# def find_closest(d, init_item):
#     '''finds closest in dictionary d to init item'''
#     min_ed = 999
#     answ_item = [-1, -1]
#     for comp_item in d.keys():
#         dist = ed.eval(init_item, comp_item)
#         if dist < min_ed:
#             min_ed = dist
#             answ_item = (min_ed, comp_item)
#
#     return answ_item


# def squash(od, t, verbose =False):
#     answ = OrderedDict()
#     sp_to_n = {}
#     index = 0
#
#     for init_item in tqdm_notebook(od.items()):
#         #ord_dict.pop(init_item[0])
#
#         if len(answ) == 0 :
#             if verbose: print("new spacer:", init_item[0], init_item[1])
#             answ[init_item[0]] = init_item[1]
#             sp_to_n[init_item[0]] = index
#             index += 1
#         else:
#             min_ed, answ_item = find_closest(answ, init_item[0])
#             if min_ed < t:
#                 if verbose: print("add:", init_item[0], "to", answ_item, )
#                 answ[answ_item] += init_item[1]
#                 sp_to_n[init_item[0]] = sp_to_n[answ_item]
#
#             else:
#                 if verbose: print("new spacer:", init_item[0], init_item[1])
#                 sp_to_n[init_item[0]] = index
#                 index += 1
#                 answ[init_item[0]] = init_item[1]
#
#     return answ, sp_to_n
#
#
# def parse_pairs(path, split = '\t', n = 50):
#     with open(path) as f:
#         pairs = [[y[:n] for y in x[:-2].split(split) ] for x in f.readlines()]
#
#     pairs = [x for x in pairs if len(x) > 1]
#     pairs = [x for x in pairs if len(x[0]) > 25 and len(x[1]) > 25]
#
#     lines = []
#     for p in pairs:
#         lines.append(p[0])
#         lines.append(p[1])
#
#     return pairs, lines


# def lines_to_ordered_dict(lines):
#     counter = Counter(lines)
#
#     ord_dict = OrderedDict()
#
#     u_lines = []
#     counts = []
#     for item in counter.items():
#         u_lines.append(item[0])
#         counts.append(item[1])
#
#     u_lines = np.array(u_lines)
#     counts = np.array(counts)
#
#     args_s = np.argsort(counts)[::-1]
#
#     for l, c in zip(u_lines[args_s], counts[args_s]):
#         ord_dict[l] = c
#
#     return ord_dict


# def get_cl_n(ord_dict, t=6):
#     sp_to_n = {}
#
#     nd, sp_to_n = squash(ord_dict, t, 0)
#
#     cl_to_n = {}
#     n_to_cl = {}
#     for i, it in enumerate(nd.items()):
#         cl_to_n[it[0]] = i
#         n_to_cl[i] = it[0]
#
#     return nd, sp_to_n, cl_to_n, n_to_cl


def process_pair(pair, cl_to_n, t = 6):
    try:
        return [cl_to_n[find_closest(cl_to_n, pair[0])[1]], cl_to_n[find_closest(cl_to_n, pair[1])[1]]]
    except:
        return [-1, -1]
    
def process_pair_t(tup):
    try:
        return [tup[1][find_closest(tup[1], tup[0][0])[1]], tup[1][find_closest(tup[1], tup[0][1])[1]]]
    except:
        return [-1, -1]
    
def process_batch(batch, cl_to_n):
    return [process_pair(p, cl_to_n) for p in batch]

    
def _copy_gen(x, n):
    for i in range(n):
        yield x

def graph_from_raw(path, split = ' ', t = 50, v=1, n_jobs=4, mp =1, cut = None):
    if v: print("reading pairs, clustering...")
    pairs, lines = parse_pairs(path,split, t)
    ord_dict = lines_to_ordered_dict(lines)
    
    if v: print("making sp_to_n...")
    nd, sp_to_n, cl_to_n, n_to_cl = get_cl_n(ord_dict)
    
    if v: print("processing pairs...")

    if not cut is None:
        pairs = pairs[:cutl]
        
    if mp:
        from multiprocessing import Pool
        with Pool(n_jobs) as pool:
            print("Using {} jobs".format(n_jobs))

            batches = np.array_split(pairs, n_jobs)
            batches_list = list(tqdm_notebook(pool.starmap(process_batch, zip(batches, _copy_gen(cl_to_n, n_jobs))), total = n_jobs))
            pairs_n = [x for y in batches_list for x in y]
    else:
        pairs_n = [process_pair(p, cl_to_n) for p in tqdm_notebook(pairs)]
        
    if v: print("making graph...")
    graph = np.zeros((len(cl_to_n),len(cl_to_n)))
    err = 0
    for p in pairs_n:
        if len(p) == 2 and sum(p) != -2:
            graph[p[0]][p[1]] += 1  
        else:
            err += 1
    
    return graph, ord_dict, sp_to_n, cl_to_n, n_to_cl, err, pairs_n






