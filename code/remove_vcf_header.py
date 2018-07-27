from __future__ import print_function
import sys
import argparse
import os.path

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputfile',required=True, help='')
    parser.add_argument('-o','--outputfile',nargs='?', help='')
    parser.add_argument('-s','--stdout', action='store_true', help='')
    args = parser.parse_args()

    of = args.outputfile
    if not os.path.isfile(args.inputfile):
        print(args.inputfile, 'doesn\'t exist', sep=" ")
        sys.exit(1)

    if args.stdout:
        of = sys.stdout

    if not args.stdout and not (args.outputfile):
        args.outputfile = args.inputfile + '.noh'
        of = open(args.outputfile,'w')

    return(args.inputfile, of)

def main():
    input_file, output_file = get_args()

    with open(input_file,'r') as f:
        for line in f:
            if not line.startswith('##'):
                print(line,file=output_file,end='')

if __name__ == '__main__':
    main()
