import numpy as np

def get_contigs(l, dist):
    if dist > len(l):
        return []
    else:
        contigs = []
        for i in range(len(l) - dist + 1):
            #print(l[i:i+dist])
            contigs.append(tuple(l[i:i+dist]))
        return contigs


def get_contigs_from_arrays(arrays, dist):
    pairs = []
    for a in arrays:
        pairs.extend(get_contigs(a, dist))
    return pairs

def iou(l1, l2):
    intersection = set(l1).intersection(set(l2))
    union  = set(l1).union(set(l2))
    return len(intersection)/len(union)


def calculate_two_sets(s1,s2,level=4):
    scores = []
    for d in range(1, level + 1):
        contigs_1 = get_contigs_from_arrays(s1, d)
        contigs_2 = get_contigs_from_arrays(s2, d)
        scores.append(iou(contigs_1,contigs_2))

    return scores, np.mean(scores)