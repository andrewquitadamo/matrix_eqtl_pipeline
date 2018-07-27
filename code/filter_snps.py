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
    args = parser.parse_args()

    if not os.path.isfile(args.vcf_input):
        print(args.vcf_input, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if not (args.output_file):
        args.output_file = args.vcf_input + '.maf_filtered'

    return(args.vcf_input, args.output_file)
    
def output(line, fo):
    if line:
        print(line, file=fo)

def main():
    vcf_input, output_file = get_args()

    with open(vcf_input, 'r') as f, open(output_file, 'w') as fo:
        for line in f:
            line = filter(line)
            output(line, fo)

if __name__ == '__main__':
    main()
