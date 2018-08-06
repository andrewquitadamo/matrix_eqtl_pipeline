from __future__ import print_function
import argparse
import os
import sys
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import DataFrame

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file', required=True, help='')
    parser.add_argument('-n','--number-factors', required=True, help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(args.input_file, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not args.output_file:
        args.output_file = args.input_file + '.peer_factors_' + args.number_factors

    return(args.input_file, args.number_factors, args.output_file)

def main():
    r = ro.r
    utils = importr('utils', robject_translations={'with': '_with'})
    write_table = utils.write_table

    r.source("code/peer_function.R")

    input_filename, num_factors, output_filename = get_args()

    factors = r['peer_function'](input_filename, num_factors)

    write_table(factors, output_filename, col_names=True, row_names=False, sep="\t", quote=False)

if __name__ == '__main__':
    main()
