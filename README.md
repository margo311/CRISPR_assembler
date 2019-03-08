#CRISPR_assembler
Code for CRISPR cas arrays assembling from results of high-throughput sequencing

This util expects file or files with pairs of spacers as input and returns assembled CRISPR arrays.
See example usage below.

VER 0.1


------------
Python usage
------------

Process read, cluster spacer and build spacer graph

.. code-block:: python

    import crispr_assembler as ca
    read = ca.Read("PATH/TO/READ")
    read.correct_errors()
    graph = read.graph_from_pairs()[0]
    ca.plot_gr(graph, log = 1, s = 10)


Restore using greedy pipeline (works ok on every dataset, can't allign spacer to more than one array)
Threashold is minimum edge weight to add.
Weights are weights of edges between spacers, not spacers occurences!

.. code-block:: python	

	arrays, weights = restore_arrays_greedy(graph, threshold)



-----
Concole usage
-----


Example input file is stored in ./test
Example script to run assembling

python PATH_TO_ASSEMBLER/src/main/run_greedy_pipeline.py 
	--pairs_path PATH_TO_ASSEMBLER/
	--pairs_names test_pairs_1.txt
	--save_path PATH_TO_SAVE
	--plot_name plot.pdf
	--error_threshold 5
	--assemble_threshold 1


