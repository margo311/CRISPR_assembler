from ..static.constants import reverse


def read_fastq(path):
    with open(path) as f:
        lines = f.readlines()

    reads = [x[:-1] for x in lines[1::4]]
    qualities = [x[:-1] for x in lines[3::4]]

    return reads, qualities


def rc(x, reverse=reverse, r=0):
    d = dict(zip(reverse.keys(), reverse.values()))
    if r:
        d["("] = ")"
        d[")"] = "("
        return ''.join([d[y] for y in x][::-1])
    else:
        return ''.join([d[y] for y in x])