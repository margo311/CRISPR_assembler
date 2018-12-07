from src.error_correction import read_class
from src.utils.utils import unwrap_nested, is_iterable_not_str
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--input', dest='pairs_path')#, required = True)
    parser.add_argument('--threshold', dest='threshold')

    args = parser.parse_args(['--input', '/home/anton/BigMac/skoltech/CRISPR_research/CRISPR_assembler/src/test/',
                              '--threshold', 'a'])

    print(args)

    read = read_class.Read(args.pairs_path)

    read.correct_errors(2)

    print(read.corrector.spacer_to_cluster_index)
    print(read.corrected_pairs)



