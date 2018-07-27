from __future__ import print_function
import sys
import collections
import argparse
import os.path
import gzip

#Overlap samples from different files.
#Takes files from command line, and overlaps based on header and sample IDs.
#Currently only works on tab-delimited files.

def find_duplicates(ids):
    from collections import Counter
    unique_ids = set(ids)
    id_count = Counter(ids)
    for id in unique_ids:
        if id_count[id] > 1:
            print(id + ' is not unique')
    raise Exception('Non-unique IDs in header')

def find_overlaps(fileobj, id_dict, pos_dict):
        #Read the header and split it
        header = fileobj.readline().rstrip()
        ids = header.split("\t")
        if len(ids) > len(set(ids)):
            find_duplicates(ids)
        #Add IDs to the ID count dictionary
        for counter, id_val in enumerate(ids):
            if id_val in id_dict:
                id_dict[id_val] += 1
            else:
                id_dict[id_val] = 1

            #Add the position of the IDs to the position dictionary
            if id_val in pos_dict:
                pos_dict[id_val] += "," + str(counter + 1)
            else:
                pos_dict[id_val] = str(counter + 1)

def extract_columns(fileobj, filename, extension, numfiles, arg, id_dict, pos_dict):
#with open(filename, 'r') as f:
        pos = []
        #Loop through the keys in the count dictionary
        for key in id_dict:
            #Only keep keys that have a count equal to the number of files
            if id_dict[key] == numfiles:
                ind = pos_dict[key].split(",")
                #Add the position of the column to the position array
                pos.append(int(ind[arg]))
        
        if arg == 0:
            pos = list(range(1,10)) + pos
        else:
            pos.insert(0,1)

        #Open the file
        if extension:
            filename = filename + extension + '.out'
        else:
            filename = filename + '.out'
        if '.gz' in str(filename):
            filename = str(filename).replace('.gz','') + '.gz'
            with gzip.open(str(filename), 'wb') as fo:
                write_file(fileobj, fo, pos)
        else:
            with open(str(filename), 'w') as fo:
                write_file(fileobj, fo, pos)

def write_file(readfile, writefile, pos):
    for line in readfile:
        #Split each line, reorder using the position array,
        #join to string and write to *.out file
        line = line.rstrip()
        temp = line.split("\t")
        new_line = [temp[y-1] for y in pos]
        new_line_str = "\t".join(new_line)
        print(new_line_str, file=writefile)

def get_extension(extension):
    if extension and '.' not in extension:
        extension = '.' + extension
    return extension

#TODO: Move args to get_args() function to debug
def get_args():
    #Set up command line arguments options
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--extension',nargs='?', help='')
    parser.add_argument('-v','--vcffile', required=True, help='')
    parser.add_argument('-g', '--expressionfile', required=True, help='')
    args = parser.parse_args()

    return(args)
    
#parser = argparse.ArgumentParser()
#   parser.add_argument('-i','--inputfile', help='')
#   parser.add_argument('-o','--outputfile',nargs='?', help='')
#   parser.add_argument('-s','--stdout', action='store_true', help='')
#   args = parser.parse_args()

def main():
    """Overlap samples"""
    #Set up command line arguments options
#    parser = argparse.ArgumentParser()
#    parser.add_argument('-e','--extension',nargs='?', help='')
    #parser.add_argument('file', nargs='*', help='Files to overlap')
#    parser.add_argument('-v','--vcffile', help='')
#    parser.add_argument('-g', '--expressionfile', help='')
#    args = parser.parse_args()

    args = get_args()

    id_dict = collections.OrderedDict()
    pos_dict = {}

#    args.extension = get_extension(args.extension)

    #Find the overlapping samples
    #Open each file from the arguments one by one
    for filename in (args.vcffile, args.expressionfile):
        if '.gz' in filename:
            with gzip.open(filename, 'rb') as f:
                find_overlaps(f, id_dict, pos_dict)
        else:
            with open(filename, 'r') as f:
                find_overlaps(f, id_dict, pos_dict)

    #print out the overlapping samples from each file
    for arg, filename in enumerate((args.vcffile, args.expressionfile)):
        if '.gz' in filename:
            with gzip.open(filename, 'rb') as f:
                extract_columns(f, filename, args.extension, 2, arg, id_dict, pos_dict)
        else:
            with open(filename, 'r') as f:
                extract_columns(f, filename, args.extension, 2, arg, id_dict, pos_dict)


if __name__ == '__main__':
    main()
