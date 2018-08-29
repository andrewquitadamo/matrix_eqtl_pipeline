from __future__ import print_function
import argparse
import os
import sys
from check_file import check_file

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--snp-pc-file', required=True, help='')
    parser.add_argument('-f','--peer-factor-file', required=True, help='')
    parser.add_argument('-o','--output-file', help='')
    parser.add_argument('-a','--additional-covariates', help='')
    parser.add_argument('-s','--stdout',action='store_true', help='')
    args = parser.parse_args()

    check_file(args.snp_pc_file)
    check_file(args.peer_factor_file)

    if not args.stdout and not args.output_file:
        direc = os.path.split(args.snp_pc_file)[0]
        args.output_file = direc + '/combined_covariates'

    return(args.snp_pc_file, args.peer_factor_file, args.output_file, args.additional_covariates)

def combine(snp_pc_file, peer_factor_file, outputfile=None, additional_file=None):
    if not outputfile:
        of = sys.stdout
    else:
        of = open(outputfile, 'w')

    if additional_file:
        af = open(additional_file,'r')
        _ = af.readline()

    with open(snp_pc_file, 'r') as spf, open(peer_factor_file, 'r') as pff:
        for line in spf:
            print(line,end='',file=of)
        _ = pff.readline()
        for line in pff:
            print(line,end='',file=of)
        if additional_file:
            for line in af:
                print(line,end='',file=of)

def main():

    snp_pc_file, peer_factor_file, outputfile, additional_file = get_args()
    combine(snp_pc_file, peer_factor_file, outputfile, additional_file)

if __name__ == '__main__':
    main()
