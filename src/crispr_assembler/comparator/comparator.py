from crispr_assembler.utils.hamiltonian_utils import search_best_alignment
from crispr_assembler.utils.utils import *
from crispr_assembler.utils.misc import rc

import editdistance as ed


class Comparator:
    def __init__(self, restored, reference, sp_to_id = None):
        self.restored = restored
        self.reference = reference
        self.sp_to_id = sp_to_id

        if sp_to_id is not None:
            for key, value in self.restored.items():
                self.restored[key] = self.array_to_ids(value)
            for key, value in self.reference.items():
                self.reference[key] = self.array_to_ids(value)

        self.results = {}
        for key in restored.keys():
            self.results[key] = None
        for key in reference.keys():
            self.results[key] = None

    def search_ays_in_b(self, a, b):
        for a_name, a_array in a.items():
            matched_parts, b_name, positions = search_best_alignment(
                a_array,
                b)

            self.results[a_name] = Match(a_name,
                                         b_name,
                                         len(matched_parts[0]) / len(a_array),
                                         len(matched_parts[1]) / len(b[b_name]),
                                         a_array,
                                         b[b_name])

    def search_ref_in_arrays(self):
        self.search_ays_in_b(self.reference, self.restored)
        self.search_ays_in_b(self.restored, self.reference)

    @staticmethod
    def load_from_path(restored_path, reference_path, sp_to_id_path, add_rc=1):
        sp_to_id = dict_from_csv(sp_to_id_path)

        for key in sp_to_id.copy():
            sp_to_id[rc(key, r=1)] = len(sp_to_id)

        restored = read_arrays_with_tags(restored_path, 1)
        reference = read_arrays_with_tags(reference_path, 0)
        return Comparator(restored, reference, sp_to_id)

    def array_to_ids(self, array):
        return [self.sp_to_id[find_closest(list(self.sp_to_id.keys()), x)[1]] for x in array]

    def print(self):
        for key, value in self.results.items():
            value.print()



class Match:
    def __init__(self, name_1, name_2, overlap_1, overlap_2, array_1, array_2):
        self.name_1 = name_1
        self.name_2 = name_2
        self.overlap_1 = overlap_1
        self.overlap_2 = overlap_2
        self.array_1 = array_1
        self.array_2 = array_2

    def print(self):
        print(f'searched name: {self.name_1}\n',
              f'found name: {self.name_2}\n',
              f'searched_overlap: {self.overlap_1}\n',
              f'found_overlap: {self.overlap_2}\n',
              f'arrs:\n{self.array_1}\n{self.array_2}\n_____________________\n')