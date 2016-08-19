#!/usr/bin/python3

# TODO: SORTING FILES LIKE NAME1.JPG, NAME12.JPG
import os
import sys
import math
from os.path import isfile, join

if len(sys.argv)>=2:
    usr_str = str(sys.argv[1])
    if len(sys.argv)==3:
        lead_zeros = int(sys.argv[2])
    else:
        lead_zeros = 1
else:
    print('Specify at least a new name.')
    exit()


# get current working directory
cwd = os.getcwd()
print('Working Dir: ' + cwd)

# get only files in directory
files_list = [ f for f in os.listdir(cwd) if isfile(join(cwd, f))]

# sort files
files_list.sort()

if lead_zeros == 1:
    lead_zeros = int(math.log10(len(files_list)))+1

# rename files dry-run
for c, f in enumerate(files_list, start=1):
    newname = usr_str + str(c).zfill(lead_zeros) + '.' + f.split('.')[-1]
    print(f + ' --> ' + newname)

# renaming
if input('Start batch rename? (y/n) ') == 'y':
    for c, f in enumerate(files_list, start=1):
        newname = usr_str + str(c).zfill(lead_zeros) + '.' + f.split('.')[-1]
        os.rename(f, newname)
    print('Done.')
else:
    print('Aborted.')
