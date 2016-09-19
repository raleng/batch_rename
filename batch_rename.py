#!/usr/bin/python3
import os
import sys
import math
from itertools import compress
from os.path import isfile, join

def sort_names(names):
    """ Sorts files by names

    Is able to handle reasonable sorting of
    NAME2.jpg
    NAME12.jpg
    """
    sorted_names = []
    lengths = sorted(list({len(name) for name in names}))
    for l in lengths:
        mask = [1 if len(n) == l else 0 for n in names]
        partial_names = sorted(list(compress(names, mask)))
        sorted_names += partial_names
    return sorted_names

def rename_with_counter(files_list, usr_str, lead_zeros):
    """ Returns list of new filenames"""
    newnames = []
    for counter, filename in enumerate(files_list, start=1):
        newname = usr_str + str(counter).zfill(lead_zeros) + '.' + filename.split('.')[-1]
        newnames.append(newname)
    return newnames

# argument handling
# first argument is the new name string
# second argument is number of leading zeros (optional)
if len(sys.argv) >= 2:
    user_str = str(sys.argv[1])
    if len(sys.argv) == 3:
        lead_zeros = int(sys.argv[2])
    else:
        lead_zeros = 1
else:
    print('Specify at least a new name.')
    exit()


# get current working directory
cwd = os.getcwd()
print('Working Dir: ' + cwd)

# get only files in directory and sort
files_list = [f for f in os.listdir(cwd) if isfile(join(cwd, f))]
files_list = sort_names(files_list)

# check how many leading zeros are necessary
lead_zeros = max(int(math.log10(len(files_list))) + 1, lead_zeros)
new_names = rename_with_counter(files_list, user_str, lead_zeros)

# renaming dry run
for old, new in zip(files_list, new_names):
    print(old + ' --> ' + new)

# actual renaming
if input('Start batch rename? (y/n) ') == 'y':
    for old, new in zip(files_list, new_names):
        os.rename(old, new)
    print('Done.')
else:
    print('Aborted.')
