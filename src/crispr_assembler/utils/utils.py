from collections import Iterable

import editdistance as ed
import numpy as np

import csv
import os

from crispr_assembler.utils.misc import rc
from crispr_assembler.utils.hamiltonian_utils import a_in_any_b
from tqdm import tqdm, tqdm_notebook

import pickle


def is_iterable_not_str(obj): return not isinstance(obj, str) and isinstance(obj, Iterable)


def unwrap_nested(nested, level = None):
    '''
    Unwraps list of list of ... on the given level
    '''

    # print(nested, level)
    if level is None:
        level = -1
    if level == 0 or (not is_iterable_not_str(nested)):
        # if isinstance(nested, str):
        #     return [nested]
        # else:
        #     return nested
        return [nested]
    else:
        unwrapped = []

        if type(nested) == type([]):
            for element in nested:
                unwrapped.extend(unwrap_nested(element, level - 1))

        return unwrapped


def revert_dict(d):
    dr = {}
    for item in d.items():
        if type(item[1]) == list:
            dr[tuple(item[1])] = item[0]
        else:
            dr[item[1]] = item[0]
    return dr


def find_closest(iterable, item):
    '''
    Finds closest in iterable d to item
    '''
    if len(iterable) == 0:
        return len(item), -1

    min_ed = ed.eval(next(iter(iterable)), item)
    iterable_elements = set(iterable)

    for target_item in iterable_elements:
        dist = ed.eval(item, target_item)
        if dist <= min_ed:
            min_ed = dist
            answ_item = (min_ed, target_item)

    return answ_item


# def find_closest_rc(d, sp, t=5):
#     answ_1 = find_closest(d, sp)
#     answ_2 = find_closest(d, ca.rc(sp, r=1))
#     if answ_1[0] < answ_2[0] and answ_1[0] <= t:
#         return answ_1
#     elif answ_2[0] <= answ_1[0] and answ_2[0] <= t:
#         return answ_2
#     else:
#         return [-1,-1]


def dict_to_csv(d, path):
    with open(path, 'w') as f:
        w = csv.writer(f)
        w.writerows(d.items())


def dict_from_csv(path):
    d = {}
    with open(path, 'r') as f:
        r = csv.reader(f)
        for row in r:
            d[row[0]] = row[1]
    return d


def graph_from_pairs(pairs, spacers_num=None, sparce=False):
    if spacers_num is None:
        spacers_num = len(set(unwrap_nested(pairs)))

    graph = np.zeros((spacers_num, spacers_num), dtype=int)

    for pair in pairs:
        graph[pair[0], pair[1]] += 1

    return graph


def graph_from_arrays(arrays, spacers_num=None, sparce=False):
    if spacers_num is None:
        spacers_num = len(set(unwrap_nested(arrays))) + 1

    graph = np.zeros((spacers_num, spacers_num), dtype=int)
    errors = 0

    for arr in arrays:
        for x,y in zip(arr, arr[1:]):
            if x < spacers_num and y < spacers_num:
                graph[x, y] += 1
            else:
                errors += 1

    return graph, errors


def write_list_of_lists(path,
                        list_of_lists,
                        transform = None,
                        separator_1 = "\n",
                        separator_2 = ", ",
                        add_ids=True):
    if transform is None:
        def transform(x): return x


    list_with_ids = []
    if add_ids:
        for id, el in enumerate(list_of_lists):
            list_with_ids.append(f'array_{id}')
            list_with_ids.append(separator_2.join(list(map(transform, el))))
    else:
        list_with_ids = [separator_2.join(list(map(transform, x))) for x in list_of_lists]

    with open(path, 'w') as f:
        f.write(separator_1.join(list_with_ids))


def transform_spacer_to_id(spacer, spacer_to_id, warn_threshold=5):
    dist, ref_spacer = find_closest(spacer_to_id.keys(), spacer)
    if dist > warn_threshold:
        print("WARNING! spacer {0} is {1} errors from the closest, returning -1 ".format(spacer, dist))
        return -1
    return spacer_to_id[ref_spacer]


def read_arrays_with_tags(path, add_rc):
    with open(path) as f:
        lines = [x[:-1] for x in f.readlines()]

    lines[1::2] = [x.replace(" ", "") for x in lines[1::2]]

    if ',' in lines[1]:
        separator = ','
    else:
        separator = '\t'

    arrays = dict(zip(lines[::2], lines[1::2]))

    if add_rc:
        for name, arr in zip(lines[::2], lines[1::2]):
            arrays[name + "_rc"] = rc(arr, r=1)

    for name, array in arrays.items():
        arrays[name] = [sp for sp in array.split(separator) if len(sp) > 0]

    return arrays


def read_num_arrays_with_tags(path, add_rc):
    arrays_str = read_arrays_with_tags(path, add_rc)

    return dict(zip(arrays_str.keys(), [list(map(int, x)) for x in arrays_str.values()]))


def array_to_ids(array, sp_to_id):
    array_idx = []
    distances = []
    for x in array:
        dist, idx = find_closest(list(sp_to_id.keys()), x)
        array_idx.append(sp_to_id[idx])
        distances.append(dist)
    #return [sp_to_id[find_closest(list(sp_to_id.keys()), x)[1]] for x in array]
    return array_idx, distances


def multiple_arrays_to_ids(arrays, sp_to_id):
    arrays_num = {}
    distances = {}
    for k,v in tqdm(arrays.items()):
        idxs, dist = array_to_ids(v, sp_to_id)
        arrays_num[k] = idxs
        distances[k] = dist

    return arrays_num, distances


def dict_to_lists(d):
    keys = sorted(list(d.keys()))
    values = [d[key] for key in keys]
    return keys, values


def map_dict(d, func_k=None, func_v=None):
    if func_k is None:
        func_k = lambda x : x
    if func_v is None:
        func_v = lambda x : x

    return dict(zip(map(func_k, d.keys()), map(func_v, d.values())))


# def calculate_cl_to_ind(arrays):
#     self.spacers_to_occurrences = \
#         self.hierarchical_clustering.get_sorted_by_occurrences(unwrap_nested(pairs))
#
#     self.cluster_to_index, self.spacer_to_cluster_index = \
#         self.hierarchical_clustering.hierarchical_clustering(
#             self.spacers_to_occurrences.keys(),
#             self.threshold
#         )
#
#     self.index_to_cluster = revert_dict(self.cluster_to_index)


def drop_subsequent_duplicates(l):
    filtered_l = []
    for el in l:
        if len(filtered_l) == 0 or el != filtered_l[-1]:
            filtered_l.append(el)
    return filtered_l


def determine_splitter(line):
    if '\t' in line:
        return '\t'
    elif ',' in line:
        return ','
    elif ' ' in line:
        return ' '
    else:
        raise print('COULD NOT DETERMINE SPLITTER. RETURN \t BY DEFAULT')
        return '\t'


def rearange(gr, order=None):
    new_gr = np.zeros_like(gr)

    # sums = np.arange(gr.shape[0])[::-1]
    if order is None:
        sums = gr.sum(0) + gr.sum(1)
        # print(sums)
        order = np.argsort(sums)[::-1]
        # print(order)

    for i in range(gr.shape[0]):
        for j in range(gr.shape[1]):
            new_gr[i, j] = gr[order[i], order[j]]

    return new_gr, order


def get_weights(gr, arrays):
    weights = []
    for a in arrays:
        w = []
        for x, y in zip(a, a[1:]):
            w.append(gr[x, y])
        weights.append(w)

    return weights


def calc_noise_ratio(gr0, gr):
    return 1 - gr[gr0>0].sum() / gr.sum(),\
           ((gr > 0).sum() - (gr0 > 0).sum()) / gr.flatten().shape[0]


def get_top_stats(graph, i, cut=10, axis=0):
    return np.array(sorted(graph[i])[::-1][:10]), np.argsort(graph[i])[::-1][:10]


def get_routes_all(graph, route, routes, vertex, cand_dict):
    candidates = cand_dict[vertex]

    if len(candidates) == 0:
        routes.append(route)
    else:
        is_final = 1
        for candidate in candidates:
            if not candidate in route:
                is_final = 0
                new_route = route[:]
                new_route.append(candidate)
                get_routes_all(graph, new_route, routes, candidate, cand_dict)
        if is_final:
            routes.append(route)


def restore_arrays_all(graph, all_starts = 0):
    start_vertexes = np.where(graph.sum(0) == 0)[0]
    cand = [np.where(graph[vertex] > 0)[0] for vertex in np.arange(graph.shape[0])]
    cand_dict = dict(zip(np.arange(graph.shape[0]), cand))
    if all_starts:
        start_vertexes = np.arange(graph.shape[0])

    answ = []

    for vertex in tqdm_notebook(start_vertexes):
        routes = []
        route = [vertex]
        get_routes_all(graph, route, routes, vertex, cand_dict)

        answ.extend(routes)

    def merge(a):
        a_s = sorted(a, key=len)[::-1]
        f_a = []
        for array in tqdm_notebook(a_s):
            if not a_in_any_b(array, f_a):
                f_a.append(array)
        return f_a

    return answ, merge(answ)


# def get_routes_limited(graph, route, routes, vertex, verbose=0):
#     candidates = np.where(graph[vertex] > 0)[0]
#     # print(candidates)
#     if len(candidates) == 0:
#         # print("a", routes)
#         if verbose:
#             print(vertex, 'no edges')
#         routes.append(route)
#     else:
#         is_final = 1
#         for candidate in candidates:
#
#             #             if (len(route) < 2 and (not candidate in route)) or ((not candidate in route) and \
#             #               (np.abs(gr[route[-1], candidate] - np.median(ca.get_weights(graph, [route])[0]) \
#             #                       / np.median(ca.get_weights(graph, [route])[0] < 0.5)))):
#             if not candidate in route:
#
#                 if len(route) > 1:
#                     # m = np.median(ca.get_weights(graph, [route])[0])
#                     weights = get_weights(graph, [route])[0]
#                     min_idx = np.argmin([abs(x - gr[route[-1], candidate]) for x in weights])
#                     m = abs(weights[min_idx] - gr[route[-1], candidate])
#                     if verbose:
#                         print(route,
#                               candidate,
#                               ca.get_weights(graph, [route])[0],
#                               gr[route[-1], candidate],
#                               m,
#                               m / min(weights[min_idx], gr[route[-1], candidate]))
#                 if (len(route) <= 1) or m / min(weights[min_idx], graph[route[-1], candidate]) < 1.5:
#                     is_final = 0
#                     new_route = [x for x in route]
#                     new_route.append(candidate)
#                     # print('n', new_route)
#                     get_routes_limited(graph, new_route, routes, candidate, verbose)
#         if is_final:
#             # print("a", routes)
#             routes.append(route)
#




# def process_path(path, save=1):
#     pairs_path = path + "/out/pairs/"
#     files = sorted(os.listdir(pairs_path))
#
#     print(pairs_path + files[0])
#
#     read = Read(pairs_path + files[0])
#     read.correct_errors(minimum_occurences=5)
#     gr = read.graph_from_pairs()[0]
#
#     ec = ca.EmbeddingsCalculator()
#     ec.make_argsorts(gr[:cut, :cut])
#     embs = ec.fit_predict(gr[:cut, :cut], njobs=32)
#
#     if save:
#         pickle.dump(read, open(path + "/read", 'wb'))
#         np.save(path + "/graph", gr)
#         np.save(path + "/embs", embs)
#
#     return read, gr, embs
#
#
# def load_processed(path):
#     return pickle.load(open(path + "/read", 'rb')), np.load(path + "/graph.npy"), np.load(path + "/embs.npy", embs)
#
#
#
# def unwrap_idx_to_spacer(idx_to_spacer):
#     values_as_list = []
#     for i in range(len(idx_to_spacer)):
#         values_as_list.append(idx_to_spacer[i])
#     return values_as_list
#
#
# def continue_steps(reads, pointers):
#     return any([pointers[i] < len(reads[i]) for i in range(len(reads))])
#
#
# def merge_reads(reads, t=1, v=1):
#     spacers_lists = [unwrap_idx_to_spacer(x) for x in
#                      reads]  # [unwrap_idx_to_spacer(x.index_to_cluster) for x in reads]
#     pointers = [0 for i in range(len(reads))]
#     merged_sp_to_idxes = {}
#     old_idx_to_new_idx = [{} for i in range(len(reads))]
#
#     curr = 0
#     while continue_steps(spacers_lists, pointers):
#         for i in range(len(reads)):
#             if pointers[i] < len(reads[i]):
#                 spacer = spacers_lists[i][pointers[i]]
#
#                 dist, closest = find_closest(merged_sp_to_idxes, spacer)
#                 if dist > t:
#                     merged_sp_to_idxes[spacer] = curr
#                     # new_sp_to_ids[i][spacer] = curr
#                     old_idx_to_new_idx[i][pointers[i]] = curr
#                     curr += 1
#                 else:
#                     old_idx_to_new_idx[i][pointers[i]] = merged_sp_to_idxes[closest]
#
#                 pointers[i] += 1
#
#                 if curr % 100 == 0:
#                     print(curr)
#
#                 if v:
#                     print(i, pointers[i], spacer, dist, merged_sp_to_idxes)  # , new_sp_to_ids[1])
#
#     return merged_sp_to_idxes, old_idx_to_new_idx