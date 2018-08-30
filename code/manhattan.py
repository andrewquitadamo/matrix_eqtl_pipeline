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
    parser.add_argument('-e', '--eqtl-output-file', required=True, help='')
    parser.add_argument('-l', '--position-file', help='')
    parser.add_argument('-p', '--pdf-file', help='')
    args = parser.parse_args()

    check_file(args.eqtl_output_file)

    return(args.eqtl_output_file, args.position_file, args.pdf_file)


def manhattan(eqtl_output_file, position_file, pdf_file):
    r = ro.r
    utils = importr('utils', robject_translations={'with': '_with'})
    write_table = utils.write_table

    r.source("code/manhattan.R")

    r['manhattan'](eqtl_output_file, position_file, pdf_file)


def main():
    eqtl_output_file, position_file, pdf_file = get_args()
    manhattan(eqtl_output_file, position_file, pdf_file)

if __name__ == '__main__':
    main()
