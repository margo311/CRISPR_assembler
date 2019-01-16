from ..datastyle.constants import reverse, IUPAC_WILDCARDS
import regex as re
from functools import reduce


def read_fastq(path, cut=None):
    if cut is None:
        with open(path) as f:
            lines = f.readlines()
    else:
        with open(path) as f:
            lines = f.readlines()[:cut * 4]

    reads = [x[:-1] for x in lines[1::4]]
    qualities = [x[:-1] for x in lines[3::4]]

    return reads, qualities


def rc(x, reverse=reverse, r=0):
    d = dict(zip(reverse.keys(), reverse.values()))
    if r:
        d["("] = ")"
        d[")"] = "("

    reverted = []
    for char in x:
        if char in d.keys():
            reverted.append(d[char])
        else:
            reverted.append(char)

    if r:
        return ''.join(reverted[::-1])
    else:
        return ''.join(reverted)


def repeat_to_re_pattern(repeat, e=2, d=IUPAC_WILDCARDS):
    re_pattern = "("
    for char in repeat:
        if char not in d.keys() and char != '(' and char != ')':
            re_pattern += char
        elif char in d.keys():
            re_pattern += "[" + "|".join(d[char]) + "]"

    re_pattern += "){e<=" + str(e) + "}"
    return re_pattern


def find(repeat, read, e=2):
    p_str = repeat_to_re_pattern(repeat, e=e)
    p = re.compile(p_str)

    return [x.span() for x in re.finditer(p, read)]


def split_read(read, repeat, quality=None, e=2, v=0):
    if quality is None:
        quality = 'Z' * len(read)

    spacers, qualities = split_read_single_direction(read,repeat,quality,e,v)
    inv = 0
    if spacers[0] == -1:
        spacers, qualities = split_read_single_direction(rc(read, r=1), repeat, quality, e, v)
        inv = 1

    return spacers, qualities, inv


def split_read_single_direction(read, repeat, quality, e=2, v=0):
    repeat, repeat_s, repeat_e = repeat.r, repeat.rs, repeat.re
    repeat_pos = find(repeat, read, e)

    if v: print(repeat_pos)
    if len(repeat_pos) == 0:
        return [-1, -1], [-1, -1]

    else:
        repeat_pos = repeat_pos[0]
        read_left = read[:repeat_pos[0]]
        q_left = quality[:repeat_pos[0]]

        read_right = read[repeat_pos[1]:]
        q_right = quality[repeat_pos[1]:]

        repeat_pos_l = find(repeat_e, read_left, e)
        if v: print(repeat_pos_l)
        if len(repeat_pos_l) == 0:
            left_spacer = -1
            left_sp_q = -1
        else:
            left_spacer = read_left[repeat_pos_l[0][1]:]
            left_sp_q = q_left[repeat_pos_l[0][1]:]

        repeat_pos_r = find(repeat_s, read_right, e)
        if v: print(repeat_pos_r)
        if len(repeat_pos_r) == 0:
            right_spacer = -1
            right_sp_q = -1
        else:
            right_spacer = read_right[:repeat_pos_r[0][0]]
            right_sp_q = q_right[:repeat_pos_r[0][0]]

        if left_spacer != -1 and len(left_spacer) <= 10:
            left_spacer = -1
        if right_spacer != -1 and len(right_spacer) <= 10:
            right_spacer = -1

        return [left_spacer, right_spacer], [left_sp_q, right_sp_q]


def determine_spacers_num(arrays, strategy='max'):
    flatten_arrays = list(reduce(lambda a,b : a+b, arrays))
    if strategy == 'max':
        return max(flatten_arrays) + 1
    else:
        return len(set(flatten_arrays))