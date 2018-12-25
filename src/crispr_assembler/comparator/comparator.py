from crispr_assembler.utils.hamiltonian_utils import search_best_alignment
from crispr_assembler.utils.utils import *
from crispr_assembler.utils.misc import rc

import editdistance as ed


class Comparator:
    def __init__(self, restored, reference, sp_to_id):
        self.restored = restored
        self.reference = reference
        self.sp_to_id = sp_to_id

        for key, value in self.results.items():
            self.results[key] = self.array_to_ids(value)
        for key, value in self.reference.items():
            self.reference[key] = self.array_to_ids(value)

        self.results = {}
        for key in restored.keys():
            self.results[key] = None
        for key in reference.keys():
            self.results[key] = None

    # def _search_ays_in_b(self, a, b):
    #     best_fits = {}
    #
    #     restored_names, restored_values = dict_to_lists(self.restored)
    #     #restored_values = [self.array_to_ids(r) for r in restored_values]
    #
    #     for a_name, a_array in a.items():
    #         matched_arrays, idx, positions = search_best_alignment(
    #             a_array,
    #             restored_values)
    #
    #         print('overlap: {0}\n'.format(1 - ed.eval(self.array_to_ids(ref_array), restored_values[idx]) /
    #                                       max(len(self.array_to_ids(ref_array)), len(restored_values[idx]))),
    #               'answ name: {0}\n'.format(ref_name),
    #               'restored name: {0}\n'.format(restored_names[idx]),
    #               f'arrs: {self.array_to_ids(ref_array), restored_values[idx]}\n')


    def search_ref_in_arrays(self):
        restored_names, restored_values = dict_to_lists(self.restored)
        # restored_values = [self.array_to_ids(r) for r in restored_values]

        for ref_name, ref_array in self.reference.items():
            matched_arrays, idx, positions = search_best_alignment(
                self.array_to_ids(ref_array),
                restored_values)

            print('overlap: {0}\n'.format(1 - ed.eval(self.array_to_ids(ref_array), restored_values[idx]) /
                                          max(len(self.array_to_ids(ref_array)), len(restored_values[idx]))),
                  'answ name: {0}\n'.format(ref_name),
                  'restored name: {0}\n'.format(restored_names[idx]),
                  f'arrs: {self.array_to_ids(ref_array), restored_values[idx]}\n')

    @staticmethod
    def load_from_path(restored_path, reference_path, sp_to_id_path):
        sp_to_id = dict_from_csv(sp_to_id_path)
        restored = read_arrays_with_tags(restored_path, 1)
        reference = read_arrays_with_tags(reference_path, 0)
        return Comparator(restored, reference, sp_to_id)

    def array_to_ids(self, array):
        return [self.sp_to_id[find_closest(list(self.sp_to_id.keys()), x)[1]] for x in array]

