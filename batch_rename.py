#!/usr/bin/python3

# TODO: SORTING FILES LIKE NAME1.JPG, NAME12.JPG
import os
import sys
import math
from os.path import isfile, join

def rename_with_counter(files_list, usr_str, lead_zeros):
    """ Returns list of new filenames"""
    newnames = []
    for counter, filename in enumerate(files_list, start=1):
        newname = usr_str + str(counter).zfill(lead_zeros) + '.' + filename.split('.')[-1]
        newnames.append(newname)
    return newnames

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
files_list.sort()

# check how many leading zeros are necessary
lead_zeros = max(int(math.log10(len(files_list))) + 1, lead_zeros)
new_names = rename_with_counter(files_list, user_str, lead_zeros)

# renaming
for old, new in zip(files_list, new_names):
    print(old + ' --> ' + new)

if input('Start batch rename? (y/n) ') == 'y':
    for old, new in zip(files_list, new_names):
        os.rename(old, new)
    print('Done.')
else:
    print('Aborted.')
