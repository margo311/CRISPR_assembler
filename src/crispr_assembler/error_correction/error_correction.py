from .hierarchical_clustering import HierarchicalClustering
from ..utils.utils import unwrap_nested, revert_dict
from collections import Counter


class ErrorCorrector:
    def __init__(self, threshold=0, minimum_occurrences=0):
        self.threshold = threshold
        self.minimum_occurrences = minimum_occurrences
        self.hierarchical_clustering = HierarchicalClustering()

        self.spacers_to_occurrences = None
        self.cluster_to_index = None
        self.spacer_to_cluster_index = None
        self.index_to_cluster = None

    def transform(self, contigs):
        contigs_idx = []
        for contig in contigs:
            contig_idx = []
            for sp in contig:
                # TODO add not yet fit
                if sp in self.spacer_to_cluster_index:
                    contig_idx.append(self.spacer_to_cluster_index[sp])
                else:
                    break
            contigs_idx.append(contig_idx)

        return contigs_idx

    def fit(self, contigs):
        self.spacers_to_occurrences = \
            self.hierarchical_clustering.get_sorted_by_occurrences(unwrap_nested(contigs), self.minimum_occurrences)

        self.cluster_to_index, self.spacer_to_cluster_index = \
            self.hierarchical_clustering.hierarchical_clustering(
                self.spacers_to_occurrences.keys(),
                self.threshold
            )

        self.index_to_cluster = revert_dict(self.cluster_to_index)

