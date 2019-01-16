import numpy as np
from crispr_assembler.utils.hamiltonian_utils import search_best_alignment
from crispr_assembler.utils.utils import *
from crispr_assembler.utils.misc import rc
from crispr_assembler import HierarchicalClustering
from functools import reduce


class CRISPRArrays:
    def __init__(self, arrays_path, cl_to_ind_path, add_rc=0):
        self.arrays_path = arrays_path
        self.cl_to_ind_path = cl_to_ind_path
        self.add_rc = add_rc

        self.arrays_nucleotides = self.load_arrays()
        self.cl_to_idx = self.load_cl_to_idx()
        self.arrays_idx = self.process_arrays()

    def load_arrays(self):
        return read_arrays_with_tags(self.arrays_path, self.add_rc)

    def load_cl_to_idx(self):
        if self.cl_to_ind_path is None:
            cl_to_idx = self.calculate_cl_to_ind()
        else:
            cl_to_idx = dict_from_csv(self.cl_to_ind_path)

        return cl_to_idx

    def process_arrays(self):
        return multiple_arrays_to_ids(self.arrays_nucleotides, self.cl_to_idx)

    def calculate_cl_to_ind(self, threshold=5):
        hierarchical_clustering = HierarchicalClustering()

        spacers_to_occurrences = \
            hierarchical_clustering.get_sorted_by_occurrences(reduce(lambda a,b:a+b,
                                                                     self.arrays_nucleotides.values()))

        cl_to_idx, _ = \
            hierarchical_clustering.hierarchical_clustering(
                spacers_to_occurrences.keys(),
                threshold
            )

        return cl_to_idx