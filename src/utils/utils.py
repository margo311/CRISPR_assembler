from collections import Iterable
import editdistance as ed


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

