from src.error_correction import read_class
from src.utils.utils import unwrap_nested, is_iterable_not_str
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run error correction on pairs')

    parser.add_argument('--input', dest='pairs_path', required = True)
    parser.add_argument('--treashold', dest='treashold')

    args = parser.parse_args()

    print(args)

    read = read_class.Read(args.pairs_path)

    #TODO tests
    print(read.pairs)
    print(read.spacers)



