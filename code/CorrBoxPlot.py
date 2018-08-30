from __future__ import print_function
import argparse
import os
import sys
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import DataFrame
from rpy2.robjects import pandas2ri
import rpy2
import numpy
from check_file import check_file


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--matrix-eqtl-results', required=True, help='')
    parser.add_argument('-g', '--genotype-file', help='')
    parser.add_argument('-e', '--gene-expression-file', help='')
    parser.add_argument('-s', '--stdout', action='store_true', help='')
    parser.add_argument('-o', '--output-file', help='')
    parser.add_argument('-p', '--pdf-file', help='')
    args = parser.parse_args()

    check_file(args.matrix_eqtl_results)

    if not args.stdout and not args.output_file:
        args.output_file = args.matrix_eqtl_results + '.corr'

    return(args.matrix_eqtl_results, args.genotype_file,
           args.gene_expression_file, args.output_file, args.pdf_file)


def corrplot(matrix_eqtl_file, genotype_file, gene_expression_file,
             output_filename=None, pdf_file=None):
    r = ro.r
    utils = importr('utils', robject_translations={'with': '_with'})
    write_table = utils.write_table

    r.source("code/CorrBoxPlotFile.R")

    if output_filename is None:
        output_filename = ""

    if pdf_file:
        visual = True
    else:
        pdf_file = ""
        visual = False

    corr = r['CorrBoxPlot'](matrix_eqtl_file, 0.05, gene_expression_file,
                            genotype_file, visual=visual, pdf_file=pdf_file)
    corr2 = pandas2ri.ri2py(corr)

    if output_filename:
        write_table(corr, output_filename, col_names=True, row_names=False,
                    quote=False, sep="\t")
    else:
        print(corr2.to_csv(index=False, sep='\t'))


def main():
    matrix_eqtl_file, genotype_file, gene_expression_file,
    output_file, pdf_file = get_args()
    corrplot(matrix_eqtl_file, genotype_file, gene_expression_file,
             output_file, pdf_file)

if __name__ == '__main__':
    main()
