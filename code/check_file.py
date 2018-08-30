from __future__ import print_function
import os
import sys


def check_file(filename):
    if not os.path.isfile(filename):
        print(filename, 'doesn\'t exist', sep=" ")
        sys.exit(1)
