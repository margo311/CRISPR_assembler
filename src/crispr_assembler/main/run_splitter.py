import argparse
from multiprocessing import Pool
from crispr_assembler.splitter.splitter import *
# from crispr_assembler.fastq_processor.fastq_processor import *
from crispr_assembler.datastyle.repeats import *
from crispr_assembler.utils.utils import *
import sys
from tqdm import tqdm


def process_by_batch(f, pool, batch_size=1, drop_last=False):
    buffer = []
    batch = []

    for line_idx, line in enumerate(f.readlines()):
        if len(batch) < batch_size:
            if len(buffer) < 4:
                buffer.append(line[:-1])
            if len(buffer) == 4:
                batch.append(buffer)
                buffer = []

        if len(batch) == batch_size:
            batch_copy = [x for x in batch]
            batch = []
            if len(batch_copy) != 0:
                yield list(pool.map(wrap_function, batch_copy))

    yield list(pool.map(wrap_function, batch))


def wrap_function(sample):
    return process_function(*sample)


def process_function(position, read_, plus, quality):
    return split_function(position, read_, plus, quality, repeat, e=3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--input', dest='input_path')
    parser.add_argument('--workers', dest='workers', type=int, default=4)
    parser.add_argument('--batch_size', dest='batch_size', type=int, default=100)
    parser.add_argument('--bacteria', dest='bacteria', default='ec')

    args = parser.parse_args()
    # args = parser.parse_args(['--pairs_path',
    #                           '/home/anton/BigMac/skoltech/CRISPR_research/data/clostr_11_12/out/pairs/',
    #                           '--pairs_names',
    #                           'CDisolate77_S11_L001_R1_001.fastq.gz_pairs.txt',
    #                           #'/home/anton/BigMac/skoltech/CRISPR_research/CRISPR_assembler/src/test/inp/test_pairs_2.txt',
    #                           '--save_path',
    #                           '/home/anton/BigMac/skoltech/CRISPR_research/data/clostr_11_12/out/restored/',
    #                           '--plot_name',
    #                           'CDisolate77_S11_L001_R1_001.pdf',
    #                           '--error_threshold',
    #                           '6',
    #                           '--assemble_threshold',
    #                           '0'
    #                           ])

    if args.bacteria == 'ec':
        repeat = ecoli_r_2
    elif args.bacteria == 'cd':
        repeat = redundant
    else:
        raise Exception("Unknown bacteria")

    # fastq_p = FastqProcessor(process_function=process_func)

    p = Pool(args.workers)

    f = open(args.input_path, 'r')

    for i, res in tqdm(enumerate(process_by_batch(f, p, args.batch_size))):
        for read in res:
            print('\t'.join(read[2]))
            print('\t'.join(read[3]))



