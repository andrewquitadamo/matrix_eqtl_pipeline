from __future__ import print_function
import sys
import argparse
import os.path
from check_file import check_file


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf-input', required=True, help='')
    parser.add_argument('-o', '--output-file', help='')
    parser.add_argument('-m', '--meqtl-output-file', help='')
    args = parser.parse_args()

    check_file(args.vcf_input)

    args.output_file = args.output_file or (
        args.vcf_input + '.positions')

    args.meqtl_output_file = args.meqtl_output_file or (args.vcf_input + '.meqtl_positions')

    return(args.vcf_input, args.output_file, args.meqtl_output_file)


def parse(line):
    fields = line.strip().split()
    if line.startswith('#'):
        return
    else:
        chr, pos, id, ref, alt, qual, filter, info, format, *genos = fields

        if not chr.isnumeric():
            return

        end, meqtl_pos, type = position(info, pos)

        return(id, chr, pos, end, type, meqtl_pos)


def parse_info(info, pos):
    info = info.split(';')

    endflag = False
    if 'SVTYPE' in info:
        if 'END' in info:
            endflag = True

    end = pos
    typeflag = False
    for counter, field in enumerate(info):
        if field.startswith('SVTYPE'):
            type = field.split('=')[-1]
            typeflag = True
        if field.startswith('VT') and typeflag is False:
            type = field.split('=')[-1]
        if endflag:
            if field.startswith('END'):
                end = field.split('=')[-1]
        else:
            if field.startswith('SVLEN'):
                end = field.split('=')[-1]
                end = str(int(pos) + int(end))

    return(type, end)


def position(info, pos):
    type, end = parse_info(info, pos)
    if pos == end:
        meqtl_pos = pos
    else:
        meqtl_pos = str(int(pos)+round((int(end)-int(pos))/2))

    return(end, meqtl_pos, type)


def main():
    filename, position_file, meqtl_position_file = get_args()
    with open(filename, 'r') as f, open(position_file, 'w') as pf, open(meqtl_position_file, 'w') as mpf:
        print("snpid\tchr\tpos", file=mpf)
        print("snpid\tchr\tstart\tend\ttype", file=pf)
        for line in f:
            position_vals = parse(line)

            if position_vals:
                id, chr, pos, end, type, meqtl_pos = position_vals
                print(id, chr, pos, end, type, sep='\t', file=pf)
                print(id, chr, meqtl_pos, sep='\t', file=mpf)

if __name__ == '__main__':
    main()
