from .hierarchical_clustering import HierarchicalClustering
from ..utils.utils import unwrap_nested, revert_dict
from collections import Counter


class ErrorCorrector:
    def __init__(self, threshold=0, minimum_occurrences=0):
        self.threshold = threshold
        self.minimum_occurrences = minimum_occurrences
        self.hierarchical_clustering = HierarchicalClustering()

    def transform(self, pairs_list):
        pairs_idx = []
        for pair in pairs_list:
            if pair[0] in self.spacer_to_cluster_index and pair[1] in self.spacer_to_cluster_index:
                pairs_idx.append([self.spacer_to_cluster_index[pair[0]], self.spacer_to_cluster_index[pair[1]]])
        return pairs_idx

    def fit(self, pairs):
        self.spacers_to_occurrences = \
            self.hierarchical_clustering.get_sorted_by_occurrences(unwrap_nested(pairs), self.minimum_occurrences)

        self.cluster_to_index, self.spacer_to_cluster_index = \
            self.hierarchical_clustering.hierarchical_clustering(
                self.spacers_to_occurrences.keys(),
                self.threshold
            )

        self.index_to_cluster = revert_dict(self.cluster_to_index)

