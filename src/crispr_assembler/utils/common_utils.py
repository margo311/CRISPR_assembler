from crispr_assembler.error_correction.read_class import Read


def restore(path, minimum_occurences = 0):
    read = Read(path)
    read.correct_errors(minimum_occurences = minimum_occurences)
    return read