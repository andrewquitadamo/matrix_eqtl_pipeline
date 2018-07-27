from __future__ import print_function
import argparse
import os
import sys

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--snppcfile', required=True, help='')
    parser.add_argument('-p','--peerfactorfile', required=True, help='')
    parser.add_argument('-o','--outputfile',nargs='?', help='')
    args = parser.parse_args()

    if not os.path.isfile(args.snppcfile):
        print(args.snppcfile, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not os.path.isfile(args.peerfactorfile):
        print(args.peerfactorfile, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not (args.outputfile):
        direc = os.path.split(args.snppcfile)[0]
        args.outputfile = direc + '/combined_covariates'

    return(args.snppcfile, args.peerfactorfile, args.outputfile)

def main():

    snp_pc_file, peer_factor_file, outputfile = get_args()

    with open(snp_pc_file, 'r') as spf, open(peer_factor_file, 'r') as pff, open(outputfile, 'w') as of:
        for line in spf:
            print(line,end='',file=of)
        _ = pff.readline()
        for line in pff:
            print(line,end='',file=of)

if __name__ == '__main__':
    main()
