from __future__ import print_function
import sys
import argparse
import os.path
from check_file import check_file

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vcf-file',required=True, help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    parser.add_argument('-s','--stdout', action='store_true', help='')
    args = parser.parse_args()

    check_file(args.vcf_file)

    if not args.stdout and not args.output_file:
        args.output_file = args.vcf_file + '.noh'

    return(args.vcf_file, args.output_file)

def remove_header(input_file, output_file=None):
    if not output_file:
        of = sys.stdout
    else:
        of = open(output_file, 'w')

    with open(input_file,'r') as f:
        for line in f:
            if not line.startswith('##'):
                print(line,file=of,end='')

def main():
    input_file, output_file = get_args()
    remove_header(input_file, output_file)

if __name__ == '__main__':
    main()
