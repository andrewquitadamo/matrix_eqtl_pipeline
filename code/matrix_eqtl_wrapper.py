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
import CorrBoxPlot
import manhattan

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
    parser.add_argument('--trans-output-file',help='')
    parser.add_argument('--trans-p-value',help='')
    parser.add_argument('--model',help='')
    parser.add_argument('--cis-distance',help='')
    parser.add_argument('--cis-p-value',help='')
    parser.add_argument('--no-header', action='store_false', help='')
    parser.add_argument('--no-rownames',action='store_false',help='')
    parser.add_argument('--missing',help='')
    parser.add_argument('--sep',help='')
    parser.add_argument('--maf',help='')
    parser.add_argument('--qqplot',help='')
    parser.add_argument('--p-value',help='')
    parser.add_argument('--eqtl-output-file',help='')
    parser.add_argument('--boxplot-pdf-file',help='')
    parser.add_argument('--correlation-output-file',help='')
    parser.add_argument('--manhattan-pdf-file',help='')

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

    return(args)

def main():

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
        vcf_file = args.filtered_filename or (vcf_file + '.maf_filtered')
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
        position_file = args.meqtl_position_filename or (vcf_file + '.meqtl_positions')
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
            sys.argv[5:] = ['-o', args.peer_factor_filename]
        print(sys.argv)
        run_peer.main()
        peer_file = args.peer_factor_filename or (gene_exp + '.peer_factors_' + args.numfactors)
        pc_file = matrix_file + '.pcs'
        sys.argv[1:] = ['-p',pc_file,'-f', peer_file]

        if args.combined_covariate_filename:
            sys.argv[5:] = ['-o', args.combined_covariate_filename]
        covariate_file = args.combined_covariate_filename or 'data/combined_covariates'
        if args.additional_covariates:
            sys.argv[len(sys.argv):] = ['-a',args.additional_covariates]
        combine_covariates.main()        

        sys.argv[1:] = ['-m',matrix_file, '-p', position_file, '-e', gene_exp, '-g', args.gene_position_file, '-c', covariate_file]

        if args.trans_output_file:
            sys.argv[len(sys.argv):] = ['--trans-output-file',args.trans_output_file] #
        if args.trans_p_value:
            sys.argv[len(sys.argv):] = ['--trans-p-value', args.trans_p_value] #
        if args.model:
            sys.argv[len(sys.argv):] = ['--model', args.model] #
        if args.cis_distance:
            sys.argv[len(sys.argv):] = ['--cis-distance', args.cis_distance] #
        if args.cis_p_value:
            sys.argv[len(sys.argv):] = ['--p-value', args.cis_p_value] #
        if args.no_header==False:
            sys.argv[len(sys.argv):] = ['--no-header'] #
        if args.no_rownames==False:
            sys.argv[len(sys.argv):] = ['--no-rownames'] #
        if args.missing:
            sys.argv[len(sys.argv):] = ['--missing', args.missing] #
        if args.sep:
            sys.argv[len(sys.argv):] = ['--sep', args.sep] #
        if args.maf:
            sys.argv[len(sys.argv):] = ['--maf', args.maf] #
        if args.qqplot:
            sys.argv[len(sys.argv):] = ['--qq-plot', args.qqplot] #
        if args.p_value:
            sys.argv[len(sys.argv):] = ['--p-value', args.p_value] #
        if args.eqtl_output_file:
            sys.argv[len(sys.argv):] = ['--output-file', args.eqtl_output_file] #

        run_matrix_eqtl.main()


        sys.argv[1:] = ['-m',args.eqtl_output_file or 'MatrixEQTLOutput','-g',matrix_file,'-e',gene_exp]

        if args.boxplot_pdf_file:
            sys.argv[len(sys.argv):] = ['--pdf-file', args.boxplot_pdf_file]
        if args.correlation_output_file:
            sys.argv[len(sys.argv):] = ['--output-file', args.correlation_output_file]
        CorrBoxPlot.main()

        if args.manhattan_pdf_file:
            sys.argv[1:] = ['-e',args.eqtl_output_file or 'MatrixEQTLOutput','-l',position_file,'-p',args.manhattan_pdf_file]
            manhattan.main()        

if __name__ == '__main__':
    main()
