import argparse
from crispr_assembler.datastyle.quality_consts import *
from tqdm import tqdm


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--input', dest='input_path')
    #parser.add_argument('--workers', dest='workers', type=int, default=4)
    #parser.add_argument('--batch_size', dest='batch_size', type=int, default=100)
    parser.add_argument('--threshold', dest='threshold', default=20)

    args = parser.parse_args()

    # args = parser.parse_args(['--input',
    #                           '/home/anton/BigMac/skoltech/CRISPR_research/article/data/ES1.merged.assembled.fastq.head',
    #                           ])

    f = open(args.input_path, 'r')

    read, quality = None, None
    for i, line in tqdm(enumerate(f.readlines())):

        if read is None:
            read = line[:-1]
        elif quality is None:
            quality = line[:-1]
        else:
            if get_lowest_q(''.join(quality.split("\t"))) > args.threshold: #TODO find splitter
                new_read = []
                for sp in read.split("\t"):
                    if len(sp) < 28 or len(sp) > 33:
                        if len(new_read) > 0:
                            print('\t'.join(new_read))
                            new_read = []
                    else:
                        new_read.append(sp)
                if len(new_read) > 0:
                    print('\t'.join(new_read))

            read, quality = line[:-1], None

            #print("line:", line, "\n", read, "\n", quality)



