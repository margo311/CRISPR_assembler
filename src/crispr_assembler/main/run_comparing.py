from crispr_assembler.assemblers.arrays_class import Arrays
from crispr_assembler.comparator.comparator import Comparator
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--path', dest='path')
    parser.add_argument('--cl_to_id', dest='cl_to_id')
    parser.add_argument('--arrays_sp', dest='arrays_sp')
    parser.add_argument('--answ_sp', dest='answ_sp')

    parser.add_argument('--output', dest='output')
    # parser.add_argument('--plot_name', dest='plot_name')
    # parser.add_argument('--error_threshold', dest='error_threshold', type=int, default=5)
    # parser.add_argument('--assemble_threshold', dest='assemble_threshold', type=int, default=0)

    #args = parser.parse_args()
    args = parser.parse_args(['--path',
                              '/home/anton/BigMac/skoltech/CRISPR_research/data/ecoli_11_12/out/restored/',
                              '--cl_to_id',
                              'Ecoli-planeA_S5_L001_R1_001_cl_to_ind',
                              '--arrays_sp',
                              'Ecoli-planeA_S5_L001_R1_001_arrays_sp',
                              '--answ_sp',
                              'answ',
                              '--output',
                              'comparing_log'
                              ])

    print(args)

    arrays = Arrays(args.path + args.arrays_sp, args.path + args.cl_to_id)
    answ = Arrays(args.path + args.answ_sp, args.path + args.cl_to_id, 1)

    comparator = Comparator(arrays, answ)

    comparator.search_ref_in_arrays()