import numpy as np

match_award = 10
mismatch_penalty = -5
gap_penalty = -10


def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty


def water(seq1, seq2):
    m, n = len(seq1), len(seq2)  # length of two sequences

    # Generate DP table and traceback path pointer matrix
    score = np.zeros((m + 1, n + 1))  # the DP table
    pointer = np.zeros((m + 1, n + 1))  # to store the traceback path

    max_score = 0  # initial maximum score in DP table
    # Calculate DP table and mark pointers
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            score_diagonal = score[i - 1][j - 1] + match_score(seq1[i - 1], seq2[j - 1])
            score_up = score[i][j - 1] + gap_penalty
            score_left = score[i - 1][j] + gap_penalty
            score[i][j] = max(0, score_left, score_up, score_diagonal)
            if score[i][j] == 0:
                pointer[i][j] = 0  # 0 means end of the path
            if score[i][j] == score_left:
                pointer[i][j] = 1  # 1 means trace up
            if score[i][j] == score_up:
                pointer[i][j] = 2  # 2 means trace left
            if score[i][j] == score_diagonal:
                pointer[i][j] = 3  # 3 means trace diagonal
            if score[i][j] >= max_score:
                max_i = i
                max_j = j
                max_score = score[i][j];

    align1, align2 = [], []  # initial sequences

    i, j = max_i, max_j  # indices of path starting point

    # traceback, follow pointers
    while pointer[i][j] != 0:
        if pointer[i][j] == 3:
            align1.append(seq1[i - 1])
            align2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif pointer[i][j] == 2:
            align1.append('-')
            align2.append(seq2[j - 1])
            j -= 1
        elif pointer[i][j] == 1:
            align1.append(seq1[i - 1])
            align2.append('-')
            i -= 1

    return seq1, seq2, align1[::-1], align2[::-1], i, max_i, j, max_j, (max_i - i) / len(seq1), (max_j - j) / len(
        seq2), max_score


def water_alignments(array, arrays_set):
    alignments = np.array([water(array, x) for x in arrays_set])
    mask = np.array([x[-1] for x in alignments]) > 10
    return alignments[mask]


def recalc_borders(alignment, seq, seq_i, seq_j, alg_i, alg_j):
    return seq_i - alg_i, (len(alignment) - alg_j) + seq_j


def preprint_seq(seq, min_border, max_border, start, end, cell_size = 4):
    seq_str = ['-']* (start - min_border) + [str(x) for x in seq] + ['-'] * (max_border - end)
    #print(seq_str)
    return ''.join([' ' + el + ' ' * (cell_size - len(el) - 1) for el in seq_str])
    #return '[' + '  '.join(seq_str_allign)+"]"


def print_alignments(alignments, seq, cell_size=4):
    # print([[align[1], seq, align[4], align[5], align[6], align[7]] for align in alignments])
    alignments_idxes = [recalc_borders(align[1], seq, align[4], align[5], align[6], align[7]) for align in alignments]

    min_border = min([x[0] for x in alignments_idxes] + [0])
    max_border = max([x[0] for x in alignments_idxes] + [len(seq)])

    printable = []
    printable.append(preprint_seq(seq, min_border, max_border, 0, len(seq)))
    for align, idx in zip(alignments, alignments_idxes):
        printable.append(preprint_seq(align[1], min_border, max_border, idx[0], idx[1]))

    return printable