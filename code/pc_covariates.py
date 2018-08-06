from __future__ import print_function
import argparse
import os
import sys
from sklearn.decomposition import IncrementalPCA
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vcf-file', required=True, help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    parser.add_argument('-n','--number-pcs',type=int,help='')
    parser.add_argument('-s','--stdout',action='store_true', help='')
    args = parser.parse_args()

    if not os.path.isfile(args.vcf_file):
        print(args.vcf_file, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not args.stdout and not args.output_file:
        args.output_file = args.vcf_file + '.pcs'

    if not (args.number_pcs):
        args.number_pcs = 1

    return(args.vcf_file, args.output_file, args.number_pcs)

def pca(genotypes, vcf_file, output_file, number_pcs):
    if not output_file:
        of = sys.stdout
    else:
        of = open(output_file, 'w')

    ipca = IncrementalPCA()
    for chunk in genotypes:
        ipca.partial_fit(chunk)

    pcs = ""

    for i in range(0,number_pcs):
        pcs = pcs + "PC" + str(i+1) + "\t" + "\t".join(str(x) for x in ipca.components_[i]) + "\n"

    with open(vcf_file, 'r') as f:
        header = f.readline().rstrip()

    print(header, file=of)
    print(pcs, end='', file=of)

def main():
    vcf_file, output_file, number_pcs = get_args()
    genotypes = pd.read_csv(vcf_file, sep = '\t', chunksize = 100000, index_col=0)
    pca(genotypes, vcf_file, output_file, number_pcs)

if __name__ == '__main__':
    main()
