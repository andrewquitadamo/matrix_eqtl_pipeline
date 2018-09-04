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
from check_file import check_file


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf-file', required=True, help='')
    parser.add_argument('-g', '--gene-expression-file', required=True, help='')
    parser.add_argument('-p', '--gene-position-file', required=True, help='')
    parser.add_argument('-n', '--numfactors', required=True, help='')
    parser.add_argument('--headless-vcf-filename', help='')
    parser.add_argument('--overlap-extension', help='')
    parser.add_argument('--maf-cutoff', help='Minor allele frequency cutoff for genotype filtering. Default is 0.05')
    parser.add_argument('--filtered-filename', help='')
    parser.add_argument('--parsed-filename', help='')
    parser.add_argument('--position-filename', help='')
    parser.add_argument('--meqtl-position-filename', help='')
    parser.add_argument('--number-pcs', help='Number of genotype principal components to correct')
    parser.add_argument('--pc-filename', help='')
    parser.add_argument('--normalized-filename', help='')
    parser.add_argument('--peer-factor-filename', help='')
    parser.add_argument('--combined-covariate-filename', help='')
    parser.add_argument('--additional-covariates', help='')
    parser.add_argument('--trans-output-file', help='')
    parser.add_argument('--trans-p-value', help='Maximum p-value for eQTL results for trans- analysis')
    parser.add_argument('--model', choices={'linear', 'anova', 'linear_cross'}, help='Model to use for eQTL analysis')
    parser.add_argument('--cis-distance', help='eQTL search window size in base pairs')
    parser.add_argument('--cis-p-value', help='Maximum p-value for eQTL results for cis- analysis')
    parser.add_argument('--no-header', action='store_false', help='')
    parser.add_argument('--no-rownames', action='store_false', help='')
    parser.add_argument('--missing', help='')
    parser.add_argument('--sep', help='Character separating fields; Default is tab')
    parser.add_argument('--maf', help='')
    parser.add_argument('--qqplot', help='')
    parser.add_argument('--eqtl-output-file', help='')
    parser.add_argument('--boxplot-pdf-file', help='')
    parser.add_argument('--correlation-output-file', help='')
    parser.add_argument('--manhattan-pdf-file', help='Filename for manhattan plot')

    args = parser.parse_args()

    check_file(args.vcf_file)
    check_file(args.gene_expression_file)
    check_file(args.gene_position_file)

    return(args)


def main():
        args = get_args()
        sys.argv[1:] = ['-v', args.vcf_file]
        sys.argv[3:] = ['-o', args.headless_vcf_filename] if args.headless_vcf_filename else []
        remove_vcf_header.main()

        vcf_file = args.headless_vcf_filename or (args.vcf_file + '.noh')
        del sys.argv[3:]
        sys.argv[2] = vcf_file
        sys.argv = sys.argv + ['-g', args.gene_expression_file]
        sys.argv[5:] = ['-e', args.overlap_extension] if args.overlap_extension else []
        vcf_overlap.main()

        gene_exp = args.gene_expression_file + args.overlap_extension if args.overlap_extension else args.gene_expression_file + '.out'
        vcf_file = vcf_file + args.overlap_extension if args.overlap_extension else vcf_file + '.out'
        del sys.argv[3:]
        sys.argv[2] = vcf_file
        sys.argv[3:] = ['-m', args.maf_cutoff] if args.maf_cutoff else []
        sys.argv[len(sys.argv):] = ['-o', args.filtered_filename] if args.filtered_filename else []
        filter_snps.main()

        del sys.argv[3:]
        vcf_file = args.filtered_filename or (vcf_file + '.maf_filtered')
        sys.argv[2] = vcf_file
        sys.argv[3:] = ['-o', args.parsed_filename] if args.parsed_filename else []
        parse.main()

        del sys.argv[3:]
        matrix_file = args.parsed_filename or (vcf_file + '.matrix')
        sys.argv[3:] = ['-o', args.position_filename] if args.position_filename else []
        sys.argv[len(sys.argv):] = ['-m', args.meqtl_position_filename] if args.meqtl_position_filename else []
        position.main()

        position_file = args.meqtl_position_filename or vcf_file + '.meqtl_positions'
        del sys.argv[3:]
        sys.argv[2] = matrix_file
        sys.argv[3:] = ['-n', args.number_pcs] if args.number_pcs else []
        sys.argv[len(sys.argv):] = ['-o', args.pc_filename] if args.pc_filename else []
        pc_covariates.main()

        sys.argv[1:] = ['-i', gene_exp]
        sys.argv[3:] = ['-o', args.normalized_filename] if args.normalized_filename else []
        run_iqn.main()

        del sys.argv[3:]
        gene_exp = args.normalized_filename or (gene_exp + '.qnorm')
        sys.argv[2] = gene_exp
        sys.argv = sys.argv + ['-n', args.numfactors]
        sys.argv[5:] = ['-o', args.peer_factor_filename] if args.peer_factor_filename else []
        run_peer.main()

        peer_file = args.peer_factor_filename or gene_exp + '.peer_factors_' + args.numfactors
        pc_file = args.pc_filename if args.pc_filename else matrix_file + '.pcs'
        sys.argv[1:] = ['-p', pc_file, '-f', peer_file]

        sys.argv[5:] = ['-o', args.combined_covariate_filename] if args.combined_covariate_filename else []
        covariate_file = args.combined_covariate_filename or 'data/combined_covariates'
        sys.argv[len(sys.argv):] = ['-a', args.additional_covariates] if args.additional_covariates else []
        combine_covariates.main()

        sys.argv[1:] = ['-m', matrix_file, '-p', position_file, '-e', gene_exp, '-g', args.gene_position_file, '-c', covariate_file]

        sys.argv[len(sys.argv):] = ['--trans-output-file', args.trans_output_file] if args.trans_output_file else []
        sys.argv[len(sys.argv):] = ['--trans-p-value', args.trans_p_value] if args.trans_p_value else []
        sys.argv[len(sys.argv):] = ['--model', args.model] if args.model else []
        sys.argv[len(sys.argv):] = ['--cis-distance', args.cis_distance] if args.cis_distance else []
        sys.argv[len(sys.argv):] = ['--p-value', args.cis_p_value] if args.cis_p_value else []
        sys.argv[len(sys.argv):] = ['--no-header'] if args.no_header is False else []
        sys.argv[len(sys.argv):] = ['--no-rownames'] if args.no_rownames is False else []
        sys.argv[len(sys.argv):] = ['--missing', args.missing] if args.missing else []
        sys.argv[len(sys.argv):] = ['--sep', args.sep] if args.sep else []
        sys.argv[len(sys.argv):] = ['--maf', args.maf] if args.maf else []
        sys.argv[len(sys.argv):] = ['--qq-plot', args.qqplot] if args.qqplot else []
        sys.argv[len(sys.argv):] = ['--output-file', args.eqtl_output_file] if args.eqtl_output_file else []

        run_matrix_eqtl.main()

        sys.argv[1:] = ['-m', args.eqtl_output_file or 'MatrixEqtlOutput', '-g', matrix_file, '-e', gene_exp]
        sys.argv[len(sys.argv):] = ['--pdf-file', args.boxplot_pdf_file] if args.boxplot_pdf_file else []
        sys.argv[len(sys.argv):] = ['--output-file', args.correlation_output_file] if args.correlation_output_file else []

        CorrBoxPlot.main()

        if args.manhattan_pdf_file:
            sys.argv[1:] = ['-e', args.eqtl_output_file or 'MatrixEqtlOutput', '-l', position_file, '-p', args.manhattan_pdf_file]
            manhattan.main()

if __name__ == '__main__':
    main()
