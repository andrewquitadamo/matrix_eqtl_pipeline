from __future__ import print_function
import sys
import argparse
import os.path

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vcf-file',required=True, help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    parser.add_argument('-s','--stdout', action='store_true', help='')
    args = parser.parse_args()

    if not os.path.isfile(args.vcf_file):
        print(args.vcf_file, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not args.stdout and not (args.output_file):
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
