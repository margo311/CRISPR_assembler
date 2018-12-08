from src.error_correction import read_class

from src.utils import plot_utils as pu

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--input_path', dest='pairs_path', required = True)
    parser.add_argument('--output_path', dest='save_path')
    parser.add_argument('--plot_path', dest='plot_path')
    parser.add_argument('--threshold', dest='threshold')

    args = parser.parse_args(['--input_path',
                              '/home/anton/BigMac/skoltech/CRISPR_research/CRISPR_assembler/src/test/inp/',
                              '--output_path',
                              '/home/anton/BigMac/skoltech/CRISPR_research/CRISPR_assembler/src/test/out/',
                              '--plot_path',
                              '/home/anton/BigMac/skoltech/CRISPR_research/CRISPR_assembler/src/test/out/plot.pdf',
                              '--threshold',
                              'a'])

    print(args)

    read = read_class.Read(args.pairs_path)

    read.correct_errors(2)

    _ = read.graph_from_pairs()

    if args.plot_path:
        print("I'm plotting to ", args.plot_path)
        pu.plot_gr(_, args.plot_path,  log = 1)

    print(read.corrector.spacer_to_cluster_index)
    print(read.corrected_pairs)
    print(read.corrector.cluster_to_index)

    read.dump(args.save_path)



