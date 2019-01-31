from crispr_assembler.utils import utils
from crispr_assembler.error_correction.error_correction import ErrorCorrector

import os

class Read:
    def __init__(self, path, names=None):
        if names is None:
            names = os.listdir(path)

        self.names = names
        self.pairs = [self._load_pairs_from_path(path + name, ' ') for name in self.names]

        self._get_spacers_set()

    def _load_pairs_from_path(self, path, split = '\t', limit = None):
        if limit is None:
            limit = 1000 #TODO fix shit

        with open(path) as f:
            pairs = [[y[:limit] for y in x[:-1].split(split)] for x in f.readlines()]

        return pairs

    def _get_spacers_set(self):
        self.spacers = set(utils.unwrap_nested(self.pairs))

    def correct_errors(self, threshold=5, minimum_occurences=0):
        self.corrector = ErrorCorrector(threshold, minimum_occurences)

        self.corrector.fit(self.pairs)
        self.corrected_pairs = list(map(self.corrector.transform, self.pairs)) #TODO questionable

        self.cluster_to_index = self.corrector.cluster_to_index
        self.spacer_to_cluster_index = self.corrector.spacer_to_cluster_index

    def graph_from_pairs(self, store=True):
        graph = utils.graph_from_pairs(utils.unwrap_nested(self.corrected_pairs, 1), len(self.corrector.cluster_to_index))

        if store:
            self.graph = graph

        return graph

    def dump(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

        names_meaningful = [name.split(".")[0] for name in self.names]

        for name, pairs_list in zip(names_meaningful, self.corrected_pairs):
            with open(path + name + "_cluster_inds", 'w') as f:
                f.write('\n'.join(['\t'.join(map(str, pair)) for pair in  pairs_list]))

        utils.dict_to_csv(self.cluster_to_index, path + names_meaningful[0] + "_cl_to_ind")
        utils.dict_to_csv(self.spacer_to_cluster_index, path + names_meaningful[0] + "_sp_to_ind")







