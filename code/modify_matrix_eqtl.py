from __future__ import print_function
import subprocess
import sys
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output-file',nargs='?', help='')
    parser.add_argument('-s','--stdout', action='store_true', help='')
    args = parser.parse_args()

    if not args.stdout and not args.output_file:
        args.output_file = 'code/MatrixEQTL.R'

    return(args.output_file)

def main():
    output_file = get_args()
    if not output_file:
        of = sys.stdout
    else:
        of = open(output_file, 'w')

    subprocess.run(["wget", "https://cran.r-project.org/src/contrib/MatrixEQTL_2.2.tar.gz"], stdout=subprocess.DEVNULL)
    subprocess.run(["tar", "-xvzf", "MatrixEQTL_2.2.tar.gz"], stdout=subprocess.DEVNULL)

    with open('MatrixEQTL/R/Matrix_eQTL_engine.R') as f:
        for line in f:
            if line.strip().startswith('message'):
                if 'matched' in line:
                    line = line.replace('message','mess = paste')
                else:
                    line = line.replace('message','mess = paste0')
                if line.strip().endswith(");"):
                    if 'rp' in line:
                        line = line.replace(");",",'\\n',sep='');")
                    else:
                        line = line.replace(");",",'\\n');")
                if 'significant' in line:
                    print(line, file=of)
                    print(next(f), file=of)
                    print('cat(mess)', file=of)
                else:
                    print(line, file=of)
                    print('cat(mess)', file=of)
            else:
                line = line.rstrip()
                print(line, file=of)

if __name__ == '__main__':
    main()
