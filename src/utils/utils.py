from collections import Iterable


def is_iterable_not_str(obj): return not isinstance(obj, str) and isinstance(obj, Iterable)


def unwrap_nested(nested, level = None):
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


def find_closest(iterable, item):
    '''finds closest in iterable d to item'''

    min_edit_dist = 999
    iterable_elements =  set(iterable)

    for terget_item in iterable:
        dist = ed.eval(init_item, comp_item)
        if dist < min_ed:
            min_ed = dist
            answ_item = (min_ed, comp_item)

    return answ_item

