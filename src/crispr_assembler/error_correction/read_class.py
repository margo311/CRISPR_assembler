from crispr_assembler.utils import utils
from crispr_assembler.error_correction.error_correction import ErrorCorrector

import os


class Read:
    def __init__(self, path, input_type='each', splitter=None):
        self.contigs = self._load_contigs(path, input_type, splitter)
        self.spacers = self._get_spacers_set()

    @staticmethod
    def _load_contigs(path, input_type, splitter=None):
        with open(path) as f:
            lines = f.readlines()

        if splitter is None:
            splitter = utils.determine_splitter(max(lines, key=len))

        if input_type == 'each':
            lines_slice = slice(0, len(lines), 1)
        else:
            lines_slice = slice(0, len(lines), 2)

        return [x[:-1].split(splitter) for x in lines[lines_slice]]

    def _get_spacers_set(self):
        return set(utils.unwrap_nested(self.contigs))

    def correct_errors(self, threshold=5, minimum_occurences=0):
        self.corrector = ErrorCorrector(threshold, minimum_occurences)

        self.corrector.fit(self.contigs)
        self.contigs_idx = self.corrector.transform(self.contigs) #TODO questionable

        self.cluster_to_index = self.corrector.cluster_to_index
        self.spacer_to_cluster_index = self.corrector.spacer_to_cluster_index

    def graph_from_pairs(self, store=True):
        #graph = utils.graph_from_pairs(utils.unwrap_nested(self.corrected_pairs, 1), len(self.corrector.cluster_to_index))
        graph = utils.graph_from_arrays(self.contigs_idx)

        if store:
            self.graph = graph

        return graph

    def dump(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

        # names_meaningful = [name.split(".")[0] for name in self.names]
        #
        # for name, pairs_list in zip(names_meaningful, self.corrected_contigs):
        #     with open(path + name + "_cluster_inds", 'w') as f:
        #         f.write('\n'.join(['\t'.join(map(str, pair)) for pair in  pairs_list]))
        #
        # utils.dict_to_csv(self.cluster_to_index, path + names_meaningful[0] + "_cl_to_ind")
        # utils.dict_to_csv(self.spacer_to_cluster_index, path + names_meaningful[0] + "_sp_to_ind")







