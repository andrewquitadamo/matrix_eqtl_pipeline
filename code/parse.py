from __future__ import print_function
import argparse
import os
import sys
from check_file import check_file


def add_genotypes(id, genos):
    for counter, geno in enumerate(genos):
        geno = geno.split(':')[0]
        if '.' in geno:
            return
        else:
            if '|' in geno:
                raw_geno = geno.split('|')
            if '/' in geno:
                raw_geno = geno.split('/')
        geno = str(int(raw_geno[0]) + int(raw_geno[1]))
        genos[counter] = geno
    line = id + '\t' + '\t'.join(genos)
    return(line)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf-input', required=True, help='')
    parser.add_argument('-o', '--output-file', help='')
    parser.add_argument('-s', '--stdout', action='store_true', help='')
    args = parser.parse_args()

    check_file(args.vcf_input)

    if not args.stdout and not args.output_file:
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


def parse_all(input_file, output_file=None):
    if not output_file:
        of = sys.stdout
    else:
        of = open(output_file, 'w')

    with open(input_file, 'r') as f:
        for line in f:
            line = parse(line)
            if line:
                print(line, file=of)


def main():
    filename, matrix_file = get_args()
    parse_all(filename, matrix_file)

if __name__ == '__main__':
    main()
