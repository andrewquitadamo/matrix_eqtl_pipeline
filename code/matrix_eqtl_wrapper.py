from __future__ import print_function
import sys
import argparse
import os.path
import remove_vcf_header
import filter_snps
import parse
import position
import vcf_overlap
import pc_covariates
import run_matrix_eqtl
import run_iqn
import run_peer
import combine_covariates

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vcf-file', required=True, help='')
    parser.add_argument('-g','--gene-expression-file', required=True, help='')
    parser.add_argument('-p','--gene-position-file', required=True, help='')
    parser.add_argument('-n','--numfactors',required=True, help='')
    args = parser.parse_args()

    if not os.path.isfile(args.vcf_file):
        print(args.vcf_file, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not os.path.isfile(args.gene_expression_file):
        print(args.gene_expression_file, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not os.path.isfile(args.gene_position_file):
        print(args.gene_position_file, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    return(args.vcf_file, args.gene_expression_file, args.gene_position_file, args.numfactors)

def main():

        vcf_file, gene_exp, gene_position, numfactors = get_args()

        sys.argv[1:] = ['-v', vcf_file]
        remove_vcf_header.main()
        vcf_file = vcf_file + '.noh'
        sys.argv[2] = vcf_file
        sys.argv = sys.argv + ['-g',gene_exp]
        vcf_overlap.main()
        gene_exp = gene_exp + '.out'
        vcf_file = vcf_file + '.out'
        del sys.argv[-2:]
        sys.argv[2] = vcf_file
        filter_snps.main()
        vcf_file = vcf_file + '.maf_filtered'
        sys.argv[2] = vcf_file
        parse.main()
        matrix_file = vcf_file + '.matrix'
        position.main()
        position_file =vcf_file + '.meqtl_positions'
        vcf_file = vcf_file + '.matrix'
        sys.argv[2] = vcf_file
        pc_covariates.main()
        sys.argv[1:] = ['-i',gene_exp]
        run_iqn.main()
        gene_exp = gene_exp + '.qnorm'
        sys.argv[2] = gene_exp
        sys.argv = sys.argv + ['-n',numfactors]
        run_peer.main()
        peer_file = gene_exp + '.peer_factors_' + numfactors
        pc_file = matrix_file + '.pcs'
        sys.argv[1:] = ['-s',pc_file,'-p', peer_file]
        combine_covariates.main()        
        covariate_file = 'data/combined_covariates'
        sys.argv[1:] = ['-m',vcf_file, '-p', position_file, '-e', gene_exp, '-g', gene_position, '-c', covariate_file]
        run_matrix_eqtl.main()
        
if __name__ == '__main__':
    main()
