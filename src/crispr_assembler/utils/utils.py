from collections import Iterable

import editdistance as ed
import numpy as np

import csv

from crispr_assembler.utils.misc import rc


def is_iterable_not_str(obj): return not isinstance(obj, str) and isinstance(obj, Iterable)


def unwrap_nested(nested, level = None):
    '''
    Unwraps list of list of ... on the given level
    '''

    # print(nested, level)
    if level is None:
        level = -1
    if level == 0 or (not is_iterable_not_str(nested)):
        if isinstance(nested, str):
            return [nested]
        else:
            return nested
    else:
        unwrapped = []

        if type(nested) == type([]):
            for element in nested:
                unwrapped.extend(unwrap_nested(element, level - 1))

        return unwrapped


def revert_dict(d):
    dr = {}
    for item in d.items():
        dr[item[1]] = item[0]
    return dr


def find_closest(iterable, item):
    '''
    Finds closest in iterable d to item
    '''
    min_ed = ed.eval(next(iter(iterable)), item)
    iterable_elements = set(iterable)

    for target_item in iterable_elements:
        dist = ed.eval(item, target_item)
        if dist <= min_ed:
            min_ed = dist
            answ_item = (min_ed, target_item)

    return answ_item


def find_closest_rc(d, sp, t=5):
    answ_1 = find_closest(d, sp)
    answ_2 = find_closest(d, ca.rc(sp, r=1))
    if answ_1[0] < answ_2[0] and answ_1[0] <= t:
        return answ_1
    elif answ_2[0] <= answ_1[0] and answ_2[0] <= t:
        return answ_2
    else:
        return [-1,-1]


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
    return [sp_to_id[find_closest(list(sp_to_id.keys()), x)[1]] for x in array]


def multiple_arrays_to_ids(arrays, sp_to_id):
    arrays_num = {}
    for k,v in arrays.items():
        arrays_num[k] = array_to_ids(v, sp_to_id)

    return arrays_num


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
