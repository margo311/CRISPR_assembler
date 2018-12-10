from src.error_correction import read_class

from src.utils import plot_utils as pu
from src.utils import hamiltonian_utils as hu

import src.utils.utils as utils
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--pairs_path', dest='pairs_path', required = True)
    parser.add_argument('--pairs_names', dest='pairs_names')

    parser.add_argument('--save_path', dest='save_path')
    parser.add_argument('--plot_name', dest='plot_name')
    parser.add_argument('--error_threshold', dest='error_threshold', type=int, default=5)
    parser.add_argument('--assemble_threshold', dest='assemble_threshold', type=int, default=0)

    args = parser.parse_args(['--pairs_path',
                              '/home/anton/BigMac/skoltech/CRISPR_research/data/student_Dvyg/EC/pairs_spget_40/',
                              '--pairs_names',
                              'DVyg25_S464_R2_001_pairs.txt',
                              #'/home/anton/BigMac/skoltech/CRISPR_research/CRISPR_assembler/src/test/inp/test_pairs_2.txt',
                              '--save_path',
                              '/home/anton/BigMac/skoltech/CRISPR_research/CRISPR_assembler/src/test/out/',
                              '--plot_name',
                              'plot.pdf',
                              '--error_threshold',
                              '5',
                              '--assemble_threshold',
                              '1'
                              ])

    print(args.pairs_names.split(" "))

    print("Hey! I'm reading reads :) ..")
    read = read_class.Read(args.pairs_path, args.pairs_names.split(" "))

    print("Now I'm correcting errors :\ ...")
    read.correct_errors(args.error_threshold)
    print("Saving to ", args.save_path)
    read.dump(args.save_path)

    print("Ok. Building graph.")
    _ = read.graph_from_pairs()

    if args.plot_name:
        print("I'm plotting to ", args.save_path + args.plot_name)
        pu.plot_gr(_, args.save_path + args.plot_name,  log=1)

    print("Finally greedy restoring arrays!")
    arrays, weights = hu.restore_arrays(read.graph, args.assemble_threshold)


    # with open(args.save_path + "arrays", 'w') as f:
    #     f.write("\n".join([",".join([str(spacer) for spacer in arr]) for arr in arrays]))

    utils.write_list_of_lists(args.save_path + args.pairs_names.split(" ")[0].split(".")[0] +"_arrays_num",
                              arrays,
                              str
                              )

    utils.write_list_of_lists(args.save_path + args.pairs_names.split(" ")[0].split(".")[0] + "_arrays_sp",
                              arrays,
                              lambda x : utils.revert_dict(read.cluster_to_index)[x]
                              )

    utils.write_list_of_lists(args.save_path + args.pairs_names.split(" ")[0].split(".")[0] + "_weights",
                              weights,
                              str
                              )

    #print(arrays, weights)
    # print(read.corrector.spacer_to_cluster_index)
    # print(read.corrected_pairs)
    # print(read.corrector.cluster_to_index)





