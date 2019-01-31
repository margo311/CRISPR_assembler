import regex as re
from ..datastyle.constants import reverse, IUPAC_WILDCARDS
from crispr_assembler import rc, drop_subsequent_duplicates


def repeat_to_re_pattern(repeat, e=2, d=IUPAC_WILDCARDS):
    re_pattern = "("
    for char in repeat:
        if char not in d.keys() and char != '(' and char != ')':
            re_pattern += char
        elif char in d.keys():
            re_pattern += "[" + "|".join(d[char]) + "]"

    re_pattern += "){e<=" + str(e) + "}"
    return re_pattern


def find(read, pattern, e=2, v=0):
    re_pattern_str = repeat_to_re_pattern(pattern, e=e)
    re_pattern = re.compile(re_pattern_str)

    return [slice(*x.span()) for x in re.finditer(re_pattern, read)]


def check_reverse_complementarity(read, pattern, e=2):
    straight_idxes = find(read, pattern, e=e)
    reverse_complementary_idxes = find(rc(read, r=1), pattern, e=e)

    is_reverse = 0
    if len(straight_idxes) < len(reverse_complementary_idxes):
        is_reverse = 1
    elif len(straight_idxes) == len(reverse_complementary_idxes):
        is_reverse = -1

    return is_reverse, straight_idxes, reverse_complementary_idxes


def split_read(read, pattern, idxes=None, e=2, v=0):
    if idxes is None:
        idxes = find(read, pattern, e=e)

    if v: print(idxes)
    if len(idxes) == 0:
        return [slice(0, len(read))]
    elif len(idxes) == 1:
        parts_idxes = []
        if idxes[0].start != 0:
            parts_idxes.append(slice(0, idxes[0].start))
        if idxes[0].stop != len(read):
            parts_idxes.append(slice(idxes[0].stop, len(read)))
    else:
        parts_idxes = []
        for pattern_idx1, pattern_idx2 in zip(idxes[:-1], idxes[1:]):
            parts_idxes.append(slice(pattern_idx1.stop, pattern_idx2.start))

        if idxes[0].start != 0:
            parts_idxes.insert(0, slice(0, idxes[0].start))
        if idxes[-1].stop != len(read):
            parts_idxes.append(slice(idxes[-1].stop, len(read)))

    #len(parts_idxes) > 0 and
    return parts_idxes


def split_read_by_repeat(read, repeat, full_repeat_idxes=None, e=2):
    full_repeat_idxes = split_read(read, repeat.rc, idxes=full_repeat_idxes, e=e)

    repeat_start_idxes = split_read(read[full_repeat_idxes[0]],
                                    repeat.re)

    repeat_end_idxes = split_read(read[full_repeat_idxes[-1]],
                                    repeat.rs)

    answer = repeat_start_idxes + full_repeat_idxes[1:-1]
    if len(repeat_end_idxes) > 0 and len(full_repeat_idxes) > 0:
        answer.append(slice(full_repeat_idxes[-1].start + repeat_end_idxes[0].start,
                            full_repeat_idxes[-1].start + repeat_end_idxes[0].stop))
    return drop_subsequent_duplicates(answer)


def split_function(position, read, plus, quality, repeat, e=2, drop_last=True):
    r, idxes_forward, idxes_reverse = check_reverse_complementarity(read, repeat.rc, e=e)

    if r == 0:
        idxes = idxes_forward
        read = read
        quality = quality
    elif r == 1:
        idxes = idxes_reverse
        read = rc(read, r=1)
        quality = quality[::-1]
    else:
        return -1, read, [read], [quality]

    splits = split_read_by_repeat(read, repeat, idxes, e=e)

    return r, read, [read[split] for split in splits], [quality[split] for split in splits]





