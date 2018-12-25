from crispr_assembler.utils.utils import transform_spacer_to_id, dict_from_csv, unwrap_nested
from crispr_assembler.utils.misc import rc

class Arrays:
    def __init__(self, arrays_path, spacer_to_id_path, add_rc=0):
        self.spacer_to_id = dict_from_csv(spacer_to_id_path)
        self.arrays_as_dictionary = self.read_as_dictionary(arrays_path, add_rc)

    def read_as_dictionary(self, path, add_rc):
        with open(path) as f:
            lines = [x[:-1] for x in f.readlines()]

        if ',' in lines[1]:
            separator = ','
        else:
            separator = '\t'

        arrays_as_dictionary_full_spacers = dict(zip(lines[::2],
                                                     [line.split(separator) for line in lines[1::2]]))

        if add_rc:
            for name, arr in zip(lines[::2], lines[1::2]):
                print(name, arr)
                arrays_as_dictionary_full_spacers[name + "_rc"] = rc(arr, r=1).split(separator)

        arrays_as_dictionary = {}
        for key, value in arrays_as_dictionary_full_spacers.items():
            arrays_as_dictionary[key] = \
                [transform_spacer_to_id(spacer, self.spacer_to_id) for spacer in value]


        return arrays_as_dictionary
