from __future__ import print_function
import argparse
import os
import sys

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--snp-pc-file', required=True, help='')
    parser.add_argument('-p','--peer-factor-file', required=True, help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    args = parser.parse_args()

    if not os.path.isfile(args.snp_pc_file):
        print(args.snp_pc_file, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not os.path.isfile(args.peer_factor_file):
        print(args.peer_factor_file, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not (args.output_file):
        direc = os.path.split(args.snp_pc_file)[0]
        args.output_file = direc + '/combined_covariates'

    return(args.snp_pc_file, args.peer_factor_file, args.output_file)

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
