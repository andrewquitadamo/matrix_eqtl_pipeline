from __future__ import print_function
import sys
import argparse
import os.path
import remove_vcf_header
import vcf_overlap
import filter_snps
import parse
import position
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
    parser.add_argument('--headless-vcf-filename',help='')
    parser.add_argument('--overlap-extension',help='')
    parser.add_argument('--maf-cutoff',help='')
    parser.add_argument('--filtered-filename',help='')
    parser.add_argument('--parsed-filename',help='')
    parser.add_argument('--position-filename',help='')
    parser.add_argument('--meqtl-position-filename',help='')
    parser.add_argument('--number-pcs',help='')
    parser.add_argument('--pc-filename',help='')
    parser.add_argument('--normalized-filename',help='')
    parser.add_argument('--peer-factor-filename',help='')
    parser.add_argument('--combined-covariate-filename',help='') 
    parser.add_argument('--additional-covariates',help='')

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

    #return(args.vcf_file, args.gene_expression_file, args.gene_position_file, args.numfactors)
    return(args)

def main():

#        vcf_file, gene_exp, gene_position, numfactors = get_args()
        args = get_args()

        sys.argv[1:] = ['-v', args.vcf_file]
        if args.headless_vcf_filename:
            sys.argv[3:] = ['-o', args.headless_vcf_filename]
        remove_vcf_header.main()
        if not args.headless_vcf_filename:
            vcf_file = args.vcf_file + '.noh'
        else:
            vcf_file = args.headless_vcf_filename
            del sys.argv[-2:]
        sys.argv[2] = vcf_file
        sys.argv = sys.argv + ['-g',args.gene_expression_file]
        #File extension option
        if args.overlap_extension:
            sys.argv[5:] = ['-e', args.overlap_extension]
        vcf_overlap.main()
        if not args.overlap_extension:
            gene_exp = args.gene_expression_file + '.out'
            vcf_file = vcf_file + '.out'
        else:
            gene_exp = args.gene_expression_file + args.overlap_extension
            vcf_file = vcf_file + args.overlap_extension
        del sys.argv[3:]
        sys.argv[2] = vcf_file
        if args.maf_cutoff:
            sys.argv[3:] = ['-m',args.maf_cutoff]
        if args.filtered_filename:
            sys.argv[len(sys.argv):] = ['-o',args.filtered_filename]
        filter_snps.main()
        if args.maf_cutoff or args.filtered_filename:
            del sys.argv[3:]
        if args.filtered_filename:
            vcf_file = args.filtered_filename
        else:
            vcf_file = vcf_file + '.maf_filtered'
        sys.argv[2] = vcf_file
        if args.parsed_filename:
            sys.argv[3:] = ['-o',args.parsed_filename]
        parse.main()
        if args.parsed_filename:
            matrix_file = args.parsed_filename
            del sys.argv[3:]
        else:
            matrix_file = vcf_file + '.matrix'
        if args.position_filename:
            sys.argv[3:] = ['-o',args.position_filename]
        if args.meqtl_position_filename:
            sys.argv[len(sys.argv):] = ['-m',args.meqtl_position_filename]
        position.main()
        if args.meqtl_position_filename:
            position_file = args.meqtl_position_filename
        else:
            position_file =vcf_file + '.meqtl_positions'
        if args.meqtl_position_filename or args.position_filename:
            del sys.argv[3:]
        sys.argv[2] = matrix_file
        if args.number_pcs:
            sys.argv[3:] = ['-n',args.number_pcs]
        if args.pc_filename:
            sys.argv[len(sys.argv):] = ['-o',args.pc_filename]
        pc_covariates.main()
        sys.argv[1:] = ['-i',gene_exp]
        if args.normalized_filename:
            sys.argv[3:] = ['-o',args.normalized_filename]
        run_iqn.main()
        if args.normalized_filename:
            del sys.argv[3:]
            gene_exp = args.normalized_filename
        else:
            gene_exp = gene_exp + '.qnorm'
        sys.argv[2] = gene_exp
        sys.argv = sys.argv + ['-n',args.numfactors]
        if args.peer_factor_filename:
            sys.argv[3:] = ['-o', args.peer_factor_filename]
        run_peer.main()
        if args.peer_factor_filename:
            peer_file = args.peer_factor_filename
        else:
            peer_file = gene_exp + '.peer_factors_' + args.numfactors
        pc_file = matrix_file + '.pcs'
        sys.argv[1:] = ['-p',pc_file,'-f', peer_file]

        if args.combined_covariate_filename:
            sys.argv[5:] = ['-o', args.combined_covariate_filename]
            covariate_file = args.combined_covariate_filename
        else:
            covariate_file = 'data/combined_covariates'
        if args.additional_covariates:
            sys.argv[len(sys.argv):] = ['-a',args.additional_covariates]
        combine_covariates.main()        

        #Output file
        #P-value
        #qq-plot
        #Trans output file
        #Trans p-value
        #Model
        #Cis distance
        #Cis p-value
        #Header
        #Rownames
        #MAF
        #missing
        #sep
        sys.argv[1:] = ['-m',matrix_file, '-p', position_file, '-e', gene_exp, '-g', args.gene_position_file, '-c', covariate_file]
        run_matrix_eqtl.main()
        
if __name__ == '__main__':
    main()
