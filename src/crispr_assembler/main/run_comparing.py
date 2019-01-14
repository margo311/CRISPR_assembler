from crispr_assembler.assemblers.arrays_class import Arrays
from crispr_assembler.comparator.comparator import Comparator
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--cl_to_id', dest='cl_to_id')
    parser.add_argument('--arrays_sp', dest='arrays_sp')
    parser.add_argument('--answ_sp', dest='answ_sp')

    parser.add_argument('--output', dest='output')
    # parser.add_argument('--plot_name', dest='plot_name')
    # parser.add_argument('--error_threshold', dest='error_threshold', type=int, default=5)
    # parser.add_argument('--assemble_threshold', dest='assemble_threshold', type=int, default=0)

    #args = parser.parse_args()
    args = parser.parse_args(['--cl_to_id',
                              '/home/anton/BigMac/skoltech/CRISPR_research/data/student_Dvyg/EC/pairs_spget_20/restored/DVyg24_S463_R2_001_pairs/' +
                              'DVyg24_S463_R2_001_pairs_cl_to_ind',
                              '--arrays_sp',
                              '/home/anton/BigMac/skoltech/CRISPR_research/data/student_Dvyg/EC/pairs_spget_20/restored/DVyg24_S463_R2_001_pairs/' +
                              'DVyg24_S463_R2_001_pairs_arrays_sp',
                              '--answ_sp',
                              #'/home/anton/BigMac/skoltech/CRISPR_research/data/ecoli_11_12/out/restored/answ',
                              '/home/anton/BigMac/skoltech/CRISPR_research/data/ecoli_11_12/out/restored/Ecoli-planeA_S5_L001_R1_001/Ecoli-planeA_S5_L001_R1_001_arrays_sp',
                              '--output',
                              'comparing_log'
                              ])

    print(args)

    comparator = Comparator.load_from_path(args.arrays_sp, args.answ_sp, args.cl_to_id)

    comparator.search_ref_in_arrays()
    comparator.print()