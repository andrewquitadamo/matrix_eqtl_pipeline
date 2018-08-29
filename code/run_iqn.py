from __future__ import print_function
import argparse
import os
import sys
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import DataFrame
import numpy
from check_file import check_file

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file', required=True, help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    parser.add_argument('-s','--stdout',action='store_true',help='')
    args = parser.parse_args()

    check_file(args.input_file)

    if not args.stdout and not args.output_file:
        args.output_file = args.input_file + '.qnorm'

    return(args.input_file, args.output_file)

def iqn(input_filename, output_filename=None):
    r = ro.r
    utils = importr('utils', robject_translations={'with': '_with'})
    write_table = utils.write_table

    r.source("code/MatrixEQTL.R")
    r.source("code/general_iqn_py.R")

    if output_filename == None:
        output_filename = ""

    normed = r['inverse_quantile_norm'](input_filename)

    write_table(normed, output_filename, col_names=True, row_names=False, quote=False, sep="\t")

def main():
    input_filename, output_filename = get_args()
    iqn(input_filename, output_filename)

if __name__ == '__main__':
    main()
