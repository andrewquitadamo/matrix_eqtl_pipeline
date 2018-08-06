from __future__ import print_function
import sys
from collections import Counter
import argparse
import os.path

def filter(line):
    line = line.rstrip()
    if line.startswith('#'):
        return(line)
    else:
        fields = line.split()
        genos = fields[9:]
        geno_count = Counter(genos)
        if len(geno_count.most_common()) == 1:
            return
        if (geno_count.most_common()[0][1]) < (len(genos)-len(genos)*0.05):
            return(line)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vcf-input', required=True, help='')
    parser.add_argument('-o','--output-file',nargs='?', help='')
    parser.add_argument('-s','--stdout', action='store_true',help='')
    args = parser.parse_args()

    if not os.path.isfile(args.vcf_input):
        print(args.vcf_input, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not args.stdout and (not args.output_file):
        args.output_file = args.vcf_input + '.maf_filtered'

    return(args.vcf_input, args.output_file)
    
def filt_all(vcf_input, output_file=None):
    if not output_file:
        of = sys.stdout
    else:
        of = open(output_file, 'w')

    with open(vcf_input, 'r') as f:
        for line in f:
            line = filter(line)
            if line:
                print(line, file=of)
    

def main():
    vcf_input, output_file = get_args()
    filt_all(vcf_input, output_file)

if __name__ == '__main__':
    main()
