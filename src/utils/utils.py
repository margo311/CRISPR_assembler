from collections import Iterable

import editdistance as ed
import numpy as np

import csv




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
    min_ed = ed.eval(iterable[0], item)
    iterable_elements = set(iterable)

    for target_item in iterable_elements:
        dist = ed.eval(item, target_item)
        if dist <= min_ed:
            min_ed = dist
            answ_item = (min_ed, target_item)

    return answ_item


def dict_to_csv(d, path):
    with open(path, 'w') as f:
        w = csv.writer(f)
        w.writerows(d.items())


def dict_from_csv(path):
    with open(path, 'r') as f:
        r = csv.reader()
        return r.readlines(path)


def graph_from_pairs(pairs, spacers_num=None, sparce=False):
    if spacers_num is None:
        spacers_num = len(set(unwrap_nested(pairs)))

    graph = np.zeros((spacers_num, spacers_num), dtype=int)

    for pair in pairs:
        graph[pair[0], pair[1]] += 1

    return graph


def write_list_of_lists(path, list_of_lists, transform = None, separator_1 = "\n", separartor_2 = ", "):
    if transform is None:
        def transform(x): return x

    with open(path, 'w') as f:
        f.write(separator_1.join([
            separartor_2.join([transform(x) for x in y]) for y in list_of_lists
        ]))