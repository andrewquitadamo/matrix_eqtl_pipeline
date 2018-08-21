from __future__ import print_function
import argparse
import os
import sys
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import DataFrame
import numpy

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--matrix-eqtl-results', required=True, help='')
    parser.add_argument('-g','--genotype-file',nargs='?', help='')
    parser.add_argument('-e','--gene-expression-file',help='')
    parser.add_argument('-s','--stdout',action='store_true',help='')
    parser.add_argument('-o','--output-file',help='')
    parser.add_argument('-p','--pdf-file',help='')
    args = parser.parse_args()

    if not os.path.isfile(args.matrix_eqtl_results):
        print(args.matrix_eqtl_results, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not args.stdout and not args.output_file:
        args.output_file = args.matrix_eqtl_results+ '.corr'

    return(args.matrix_eqtl_results, args.genotype_file, args.gene_expression_file, args.output_file)

def corrplot(matrix_eqtl_file, genotype_file, gene_expression_file, output_filename=None):
    r = ro.r
    utils = importr('utils', robject_translations={'with': '_with'})
    write_table = utils.write_table

    r.source("code/CorrBoxPlotFile.R")

    if output_filename == None:
        output_filename = ""

    corr = r['CorrBoxPlot'](matrix_eqtl_file, 0.05, gene_expression_file, genotype_file)

    write_table(corr, output_filename, col_names=True, row_names=False, quote=False, sep="\t")

def main():
#    input_filename, output_filename = get_args()
#    iqn(input_filename, output_filename)
    matrix_eqtl_file, genotype_file, gene_expression_file, output_file = get_args()
    corrplot(matrix_eqtl_file, genotype_file, gene_expression_file, output_file)

if __name__ == '__main__':
    main()
