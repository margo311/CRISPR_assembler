# CRISPR_assembler
Code for CRISPR cas arrays assembling from results of high-throughput sequencing

This utilit expects file or files with pairs of spacers as input and returns assembled CRISPR arrays.
See example usage below.

VER 0.0


Example input file is stored in ./test
Example script to run assembling

python PATH_TO_ASSEMBLER/src/main/run_greedy_pipeline.py 
	--pairs_path PATH_TO_ASSEMBLER/
	--pairs_names test_pairs_1.txt
	--save_path PATH_TO_SAVE
	--plot_name plot.pdf
	--error_threshold 5
	--assemble_threshold 1


