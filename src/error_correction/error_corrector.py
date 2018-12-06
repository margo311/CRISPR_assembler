import editdistance as ed
import numpy as np
from tqdm import tqdm_notebook
from collections import Counter, OrderedDict


class ErrorCorrector:
    def __init__(self, threshold):
        self.threshold = threshold

    def hierarchical_clustering(self, iterable):
        pass

    @staticmethod
    def get_sorted_by_occurrences(self, iterable):
        counter = Counter(iterable)
        ord_dict = OrderedDict()

        elements = np.array([x for x in counter.keys()])
        counts = np.array([x for x in counter.items()])

        args_s = np.argsort(counts)[::-1]

        for element, count in zip(elements[args_s], counts[args_s]):
            ord_dict[element] = count

        return ord_dict



