from crispr_assembler.error_correction import read_class
from crispr_assembler.utils import plot_utils as pu
from crispr_assembler.utils import hamiltonian_utils as hu

import crispr_assembler.utils as utils
import argparse
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--path', dest='path', required = True)
    parser.add_argument('--save_path', dest='save_path')
    parser.add_argument('--plot_name', dest='plot_name')
    parser.add_argument('--plot_cut', dest='plot_cut', type=int, default=0)
    parser.add_argument('--graph_name', dest='graph_name', default=None)
    parser.add_argument('--min_occurrences', dest='min_occurrences', type=int, default=0)
    parser.add_argument('--error_threshold', dest='error_threshold', type=int, default=5)
    parser.add_argument('--assemble_threshold', dest='assemble_threshold', type=int, default=0)

    args = parser.parse_args()
    # args = parser.parse_args(['--path',
    #                           '/home/anton/BigMac/skoltech/CRISPR_research/crispr_assembler/test/inp/test_pairs_1.txt',
    #                           '--save_path',
    #                           '/home/anton/BigMac/skoltech/CRISPR_research/crispr_assembler/test/out/',
    #                           '--plot_name',
    #                           '322.pdf',
    #                           '--error_threshold',
    #                           '1',
    #                           '--assemble_threshold',
    #                           '0'
    #                           ])



    print("Hey! I'm reading reads :) ..")
    read = read_class.Read(args.path)

    print("Now I'm correcting errors :\ ...")
    read.correct_errors(args.error_threshold, args.min_occurrences)
    print("Saving to ", args.save_path)
    read.dump(args.save_path)

    print("Ok. Building graph.")
    graph = read.graph_from_pairs()

    if args.plot_name:
        plot_mask = graph.sum(0) >= args.plot_cut

        print("I'm plotting to ", args.save_path + args.plot_name)
        pu.plot_gr(graph[plot_mask][:, plot_mask], args.save_path + args.plot_name, all_ticks=1, log=1)

    if args.graph_name is not None:
        np.save(args.save_path+args.graph_name, graph)


    print("Finally greedy restoring arrays!")
    arrays, weights = hu.restore_arrays(read.graph, args.assemble_threshold)


    # with open(args.save_path + "arrays", 'w') as f:
    #     f.write("\n".join([",".join([str(spacer) for spacer in arr]) for arr in arrays]))

    utils.write_list_of_lists(args.save_path + args.path.split("/")[-1].split(".")[0] +"_arrays_num",
                              arrays,
                              str,
                              separator_1="\n"
                              )

    utils.write_list_of_lists(args.save_path + args.path.split("/")[-1].split(".")[0] + "_arrays_sp",
                              arrays,
                              lambda x : utils.revert_dict(read.cluster_to_index)[x],
                              separator_1="\n"
                              )

    utils.write_list_of_lists(args.save_path + args.path.split("/")[-1].split(".")[0] + "_weights",
                              weights,
                              str,
                              separator_1="\n"
                              )

    print("\n", args.path.split("/")[-1], "\n", sum([x for y in weights for x in y]) / read.graph.sum())


    #print(arrays, weights)
    # print(read.corrector.spacer_to_cluster_index)
    # print(read.corrected_pairs)
    # print(read.corrector.cluster_to_index)





