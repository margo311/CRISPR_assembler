from .hierarchical_clustering import HierarchicalClustering
from ..utils.utils import unwrap_nested, revert_dict
from collections import Counter


class ErrorCorrector:
    def __init__(self, threshold=0, minimum_occurrences=0):
        self.threshold = threshold
        self.minimum_occurrences = minimum_occurrences
        self.hierarchical_clustering = HierarchicalClustering()

    def transform(self, pairs_list):
        return [[self.spacer_to_cluster_index[pair[0]], self.spacer_to_cluster_index[pair[1]]] for pair in pairs_list]

    def fit(self, pairs):
        self.spacers_to_occurrences = \
            self.hierarchical_clustering.get_sorted_by_occurrences(unwrap_nested(pairs))

        self.cluster_to_index, self.spacer_to_cluster_index = \
            self.hierarchical_clustering.hierarchical_clustering(
                self.spacers_to_occurrences.keys(),
                self.threshold
            )

        self.index_to_cluster = revert_dict(self.cluster_to_index)


        # pairs_to_cluster_index = self._pairs_to_cluster_index(pairs, spacer_to_cluster_index)
        #
        #
        # return pairs_to_cluster_index, cluster_to_index, index_to_cluster, spacer_to_cluster_index
