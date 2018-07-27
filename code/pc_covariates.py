from __future__ import print_function
import argparse
import os
from sklearn.decomposition import IncrementalPCA
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputfile', required=True, help='')
    parser.add_argument('-o','--outputfile',nargs='?', help='')
    args = parser.parse_args()

    if not os.path.isfile(args.inputfile):
        print(args.inputfile, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not (args.outputfile):
        args.outputfile = args.inputfile + '.pcs'

    return(args.inputfile, args.outputfile)


def main():
    inputfile, outputfile = get_args()

    genotypes = pd.read_csv(inputfile, sep = '\t', chunksize = 100000, index_col=0)

    ipca = IncrementalPCA()
    for chunk in genotypes:
        ipca.partial_fit(chunk)

    pc1 = ipca.components_[0]

    pc1='PC1\t' + '\t'.join(str(x) for x in pc1)

    with open(inputfile, 'r') as f:
        header = f.readline().rstrip()

    with open(outputfile,'w') as f:
        print(header, file=f)
        print(pc1, file=f)

if __name__ == '__main__':
    main()
