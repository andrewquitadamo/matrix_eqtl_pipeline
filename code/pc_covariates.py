from __future__ import print_function
import argparse
import os
from sklearn.decomposition import IncrementalPCA
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vcf-file', required=True, help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    args = parser.parse_args()

    if not os.path.isfile(args.vcf_file):
        print(args.vcf_file, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not (args.output_file):
        args.output_file = args.vcf_file + '.pcs'

    return(args.vcf_file, args.output_file)

#TODO: Add option for number of pcs

def main():
    vcf_file, output_file = get_args()

    genotypes = pd.read_csv(vcf_file, sep = '\t', chunksize = 100000, index_col=0)

    ipca = IncrementalPCA()
    for chunk in genotypes:
        ipca.partial_fit(chunk)

    pc1 = ipca.components_[0]

    pc1='PC1\t' + '\t'.join(str(x) for x in pc1)

    with open(vcf_file, 'r') as f:
        header = f.readline().rstrip()

    with open(output_file,'w') as f:
        print(header, file=f)
        print(pc1, file=f)

if __name__ == '__main__':
    main()
