from __future__ import print_function
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import sys
import io
import argparse
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--genotype-matrix', required=True, help='')
    parser.add_argument('-p','--genotype-positions', required=True, help='')
    parser.add_argument('-e','--gene-expression-matrix', required=True, help='')
    parser.add_argument('-g','--gene-positions', required=True, help='')
    parser.add_argument('-c','--covariates', help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    parser.add_argument('-v','--p-value',type=float,nargs='?', help='')
    parser.add_argument('-q','--qq-plot',nargs='?', help='')
    args = parser.parse_args()

    if not os.path.isfile(args.genotype_matrix):
        print(args.genotype_matrix, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not args.output_file:
        args.output_file = 'MatrixEqtlOutput'

    if not args.qq_plot:
        args.qq_plot = 'MatrixEqtlQQPlot.pdf'

    if not args.p_value:
        args.p_value = 0.05

    return(args.genotype_matrix, args.genotype_positions, args.gene_expression_matrix, args.gene_positions, args.covariates, args.output_file, args.p_value, args.qq_plot)

def main():

    genotype_matrix, genotype_positions, gene_expression_matrix, gene_positions, covariates, output_file, pval,qqplot = get_args()

    r = ro.r

    r.source("code/mxeqtl.R")
    r.source("tme.R")
    #r.source("ttmet.R")

    r.mxeqtl(genotype_matrix,genotype_positions,gene_expression_matrix,gene_positions,covariates=covariates,cis_output_file=output_file,cis_pval=pval,qq=qqplot)

if __name__ == '__main__':
    main()
