from __future__ import print_function
import argparse
import os
import sys

def add_genotypes(id, genos):
    for counter, geno in enumerate(genos):
        geno = geno.split(':')[0]
        if '.' in geno:
            geno = "NA"
        else:
            raw_geno = geno.split('|')
        geno = str(int(raw_geno[0]) + int(raw_geno[1]))
        genos[counter] = geno
    line = id + '\t' + '\t'.join(genos)
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
        args.output_file = args.vcf_input + '.matrix'

    return(args.vcf_input, args.output_file)

def parse(line):
    fields = line.strip().split()
    if line.startswith('#'):
        header = 'snpid\t' + '\t'.join(fields[9:])
        return(header)
    else:
        chr, _, id, _, _, _, _, _, _, *genos = fields

        if not chr.isnumeric():
            return

        line = add_genotypes(id, genos)
        return(line)

def main():
    filename, matrix_file = get_args()
    with open(filename, 'r') as f, open(matrix_file, 'w') as mf:
        for line in f:
            line = parse(line)
            if line:
                print(line, file=mf)

if __name__ == '__main__':
    main()
