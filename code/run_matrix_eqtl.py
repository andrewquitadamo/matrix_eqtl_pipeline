from __future__ import print_function
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import sys
import io
import argparse
import os
from check_file import check_file

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--genotype-matrix', required=True, help='')
    parser.add_argument('-p','--genotype-positions', required=True, help='')
    parser.add_argument('-e','--gene-expression-matrix', required=True, help='')
    parser.add_argument('-g','--gene-positions', required=True, help='')
    parser.add_argument('-c','--covariates', help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    parser.add_argument('-v','--p-value',type=float,default=0.05, help='')
    parser.add_argument('-q','--qq-plot',nargs='?', help='')
    parser.add_argument('--trans-output-file', default="", help='')
    parser.add_argument('--trans-p-value', type=float,default=0.0, help='')
    parser.add_argument('--model', default='linear', choices={'linear','anova','linear_cross'},help='')
    parser.add_argument('--cis-distance', type=float, default=1e6, help='')
    parser.add_argument('--maf', default=0.0, help='')
    parser.add_argument('--no-header',action='store_false', help='')
    parser.add_argument('--no-rownames',action='store_false', help='')
    parser.add_argument('--missing',default='NA',help='') 
    parser.add_argument('--sep',default='\t',help='')

    args = parser.parse_args()

    check_file(args.genotype_matrix)

    return(args)

def main():

    args = get_args()

    r = ro.r

    r.source("code/mxeqtl.R")
    r.source("code/MatrixEQTL.R")

    r.mxeqtl(args.genotype_matrix,args.genotype_positions,args.gene_expression_matrix,args.gene_positions,covariates=args.covariates,cis_output_file=args.output_file,cis_pval=args.p_value, trans_output_file=args.trans_output_file, trans_pval=args.trans_p_value, cis_dist=args.cis_distance, MAF=args.maf, qq=args.qq_plot, model = args.model, header=args.no_header, rownames=args.no_rownames, missing=args.missing, sep=args.sep)

if __name__ == '__main__':
    main()
