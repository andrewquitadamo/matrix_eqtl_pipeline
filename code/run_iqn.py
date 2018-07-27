from __future__ import print_function
import argparse
import os
import sys
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import DataFrame

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputfile', required=True, help='')
    parser.add_argument('-o','--outputfile',nargs='?', help='')
    args = parser.parse_args()

    if not os.path.isfile(args.inputfile):
        print(args.inputfile, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not (args.outputfile):
        args.outputfile = args.inputfile + '.qnorm'

    return(args.inputfile, args.outputfile)


def main():
    r = ro.r
    utils = importr('utils', robject_translations={'with': '_with'})
    write_table = utils.write_table

    r.source("tme.R")
    r.source("code/general_iqn_py.R")

    input_filename, output_filename = get_args()

    normed = r['inverse_quantile_norm'](input_filename)

    write_table(normed, output_filename, col_names=True, row_names=False, quote=False, sep="\t")

if __name__ == '__main__':
    main()
