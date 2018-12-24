from crispr_assembler.utils.hamiltonian_utils import search_best_alignment
import editdistance as ed


class Comparator:
    def __init__(self, arrays, reference):
        self.arrays = reference
        self.reference = arrays
        #TODO FIX THIS BAD STUFF
    def search_ref_in_arrays(self):
        for ref_name, ref_array in self.reference.arrays_as_dictionary.items():
            matched_arrays, idx, positions = search_best_alignment(
                ref_array,
                list(self.arrays.arrays_as_dictionary.values()))

            print('overlap: {0}\n'.format(1 - ed.eval(*matched_arrays) / len(matched_arrays[0])),
                  'answ name: {0}\n'.format(ref_name),
                  'restored name: {0}\n'.format(list(self.arrays.arrays_as_dictionary.keys())[idx]),
                  f'arrs: {matched_arrays}\n')

