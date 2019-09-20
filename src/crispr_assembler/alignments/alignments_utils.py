import numpy as np

match_award = 10
mismatch_penalty = -10
gap_penalty = -10


def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return 0#gap_penalty
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
            if seq2[j - 1] == '-':
                score_up = score[i][j - 1] + 0#gap_penalty
            else:
                score_up = score[i][j - 1] +  gap_penalty

            if seq1[i - 1] == '-':
                score_left = score[i - 1][j] + 0#gap_penalty
            else:
                score_left = score[i - 1][j] +  gap_penalty
            #score_left = score[i - 1][j] + gap_penalty
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
        seq2), max_score#, score, pointer



def water_alignments(array, arrays_set, t = 10):
    alignments = np.array([water(array, x) for x in arrays_set])
    mask = np.array([x[-1] for x in alignments]) > t
    return alignments[mask]


def water_alignments_dict(array, arrays_dict, t = 10):
    alignments = dict()
    for k, v in arrays_dict.items():
        alignment = water(array, v)
        if alignment[-1] > t:
            alignments[k] = alignment
    #mask = np.array([x[-1] for x in alignments]) > t
    return alignments


def recalc_borders(alignment):
    return alignment[4] - alignment[6], (len(alignment[1]) - alignment[7]) + alignment[5]


def process_alignment(alignment, v=0):
    def upd_back(s, init_s, i):
        if i >= 0:
            s.insert(0, init_s[i])
        else:
            s.insert(0, '-')

    def upd_frwd(s, init_s, i):
        if i < len(init_s):
            s.append(init_s[i])
        else:
            s.append('-')

    init_seq = alignment[0]
    init_target = alignment[1]

    seq = alignment[2]
    target = alignment[3]

    back_ind = 1
    seq_pos = alignment[4]
    target_pos = alignment[6]
    while seq_pos - back_ind >= 0 or target_pos - back_ind >= 0:
        if v: print("b", seq, target, init_seq, init_target, seq_pos, back_ind)
        upd_back(seq, init_seq, seq_pos - back_ind)
        upd_back(target, init_target, target_pos - back_ind)
        back_ind += 1

    forward_ind = 0
    seq_pos = alignment[5]
    target_pos = alignment[7]
    while seq_pos + forward_ind < len(init_seq) or target_pos + forward_ind < len(init_target):
        if v: print("f", seq, target, init_seq, init_target, seq_pos, forward_ind)
        upd_frwd(seq, init_seq, seq_pos + forward_ind)
        upd_frwd(target, init_target, target_pos + forward_ind)
        forward_ind += 1

    return seq, target


def process_multiple_alignments(alignments):
    return [process_alignment(x) for x in alignments]


def preprint_seq(seq, cell_size = 4):
    return ''.join([' ' + str(el) + ' ' * (cell_size - len(str(el)) - 1) + ',' for el in seq])


def preprint_multiple_alignments(pa, v=0):
    def check_pointers(pointers, pa):
        return any([x < len(y[0]) for x, y in zip(pointers, pa)])

    pointers = np.zeros(len(pa)).astype(int)
    seq = []
    targets = [[] for i in range(len(pa))]

    stop = 0
    while check_pointers(pointers, pa) and stop < 100:
        curr_symbols_seq = []
        for x, p in zip(pa, pointers):
            if p < len(x[0]):
                curr_symbols_seq.append(x[0][p])
            else:
                curr_symbols_seq.append('end')

        mask = [x == '-' for x in curr_symbols_seq]
        if any(mask):
            seq.append('-')
            for i in range(len(targets)):
                if mask[i] and pointers[i] < len(pa[i][1]):
                    targets[i].append(pa[i][1][pointers[i]])
                else:
                    targets[i].append('-')

            pointers[mask] += 1

        else:
            if len(set(curr_symbols_seq)) == 1:
                seq.append(curr_symbols_seq[0])

                for i in range(len(targets)):
                    if pointers[i] < len(pa[i][1]):
                        targets[i].append(pa[i][1][pointers[i]])
                    else:
                        targets[i].append('-')

                pointers += 1
            else:
                print("asasas", seq, curr_symbols_seq)

        if v:
            print(preprint_seq(seq))
            for x in targets:
                print(preprint_seq(x))

            print(pointers, [len(x[0]) for x in pa], )
            print("-----")

        stop += 1

    return seq, targets


def preprint_multiple_alignments2(pa, v=0):
    def check_pointers(pointers, pa):
        return any([x < len(y[0]) for x, y in zip(pointers, pa)])

    pointers = np.zeros(len(pa)).astype(int)
    seq = []
    targets = [[] for i in range(len(pa))]

    stop = 0
    while check_pointers(pointers, pa) and stop < 100:
        curr_symbols_seq = []
        for x, p in zip(pa, pointers):
            if p < len(x[0]):
                curr_symbols_seq.append(x[0][p])
            else:
                curr_symbols_seq.append('end')

        mask = [x == '-' for x in curr_symbols_seq]
        if any(mask):
            seq.append('-')
            for i in range(len(targets)):
                if mask[i] and pointers[i] < len(pa[i][1]):
                    targets[i].append(pa[i][1][pointers[i]])
                else:
                    targets[i].append('-')

            pointers[mask] += 1

        else:
            if len(set(curr_symbols_seq)) == 1:
                seq.append(curr_symbols_seq[0])

                for i in range(len(targets)):
                    if pointers[i] < len(pa[i][1]):
                        targets[i].append(pa[i][1][pointers[i]])
                    else:
                        targets[i].append('-')

                pointers += 1
            else:
                print("asasas", seq, curr_symbols_seq)

        if v:
            print(preprint_seq(seq))
            for x in targets:
                print(preprint_seq(x))

            print(pointers, [len(x[0]) for x in pa], )
            print("-----")

        stop += 1

    return seq, targets
# def recalc_borders(alignment, seq, seq_i, seq_j, alg_i, alg_j):
#     return seq_i - alg_i, (len(alignment) - alg_j) + seq_j
#
#
# def preprint_seq(seq, min_border, max_border, start, end, cell_size = 4):
#     seq_str = ['-']* (start - min_border) + [str(x) for x in seq] + ['-'] * (max_border - end)
#     #print(seq_str)
#     return ''.join([' ' + el + ' ' * (cell_size - len(el) - 1) + ',' for el in seq_str])
#     #return '[' + '  '.join(seq_str_allign)+"]"
#
#
#
# def print_alignments(alignments, seq, cell_size=4):
#     # print([[align[1], seq, align[4], align[5], align[6], align[7]] for align in alignments])
#     alignments_idxes = [recalc_borders(align[1], seq, align[4], align[5], align[6], align[7]) for align in alignments]
#
#     min_border = min([x[0] for x in alignments_idxes] + [0])
#     max_border = max([x[0] for x in alignments_idxes] + [len(seq)])
#
#     printable = []
#     printable.append(preprint_seq(seq, min_border, max_border, 0, len(seq)))
#     for align, idx in zip(alignments, alignments_idxes):
#         printable.append(preprint_seq(align[1], min_border, max_border, idx[0], idx[1]))
#
#     return printable