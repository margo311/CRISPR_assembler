import numpy as np

from collections import Counter, OrderedDict
from ..utils.utils import find_closest


class HierarchicalClustering:
    def __init__(self):
        pass

    @staticmethod
    def get_sorted_by_occurrences(iterable, min_occurences):
        counter = Counter(iterable)
        ord_dict = OrderedDict()

        elements = np.array([x for x in counter.keys()])
        counts = np.array([x for x in counter.values()])

        mask = counts > min_occurences

        elements, counts = elements[mask], counts[mask]

        args_s = np.argsort(counts)[::-1]

        for element, count in zip(elements[args_s], counts[args_s]):
            ord_dict[element] = count

        return ord_dict


    @staticmethod
    def hierarchical_clustering(sorted_iterable, threshold, verbose=False):
        clusters_to_index = {}
        item_to_cluster_index = {}
        cluster_index = 0

        for item in sorted_iterable:
            if len(clusters_to_index) == 0:
                #if verbose: print("new spacer:", init_item[0], init_item[1])
                clusters_to_index[item] = cluster_index
                item_to_cluster_index[item] = cluster_index
                cluster_index += 1
            else:
                min_edit_distance, reference_cluster = find_closest(list(clusters_to_index.keys()), item)
                if min_edit_distance <= threshold:
                    #if verbose: print("add:", init_item[0], "to", cluster_item, )
                    #clusters[answ_item] += init_item[1]
                    item_to_cluster_index[item] = clusters_to_index[reference_cluster]
                else:
                    #if verbose: print("new spacer:", init_item[0], init_item[1])
                    clusters_to_index[item] = cluster_index
                    item_to_cluster_index[item] = cluster_index
                    cluster_index += 1

        return clusters_to_index, item_to_cluster_index






