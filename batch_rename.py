#!/usr/bin/python3
import begin
import getpass
import math
import os
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
    for count, fname in enumerate(files_list, start=1):
        file_count = str(count).zfill(lead_zeros)
        file_ext = fname.split('.')[-1]
        new = '{}{}.{}'.format(usr_str, file_count, file_ext)
        yield new

@begin.start
def batch_rename(user_str, *, lead_zeros=1):
    """ Batch renaming of all files in current directory

    Takes one positional argument
    user_str: new file name

    Takes one keyword argument
    lead_zeros: number of leading zeros (default=1)
    """

    # get current working directory
    cwd = os.getcwd()
    print('Working Dir: {}'.format(cwd))

    # just a little sanity check
    if cwd == '/home/{}'.format(getpass.getuser()):
        print('Ehm, no?')
        exit()

    # get only files in directory and sort
    files_list = [f for f in os.listdir(cwd) if isfile(join(cwd, f))]
    files_list = sort_names(files_list)

    # check how many leading zeros are necessary
    lead_zeros = max(int(math.log10(len(files_list))) + 1, lead_zeros)
    new_names = list(rename_with_counter(files_list, user_str, lead_zeros))

    # renaming dry run
    for old, new in zip(files_list, new_names):
        print('{old} --> {new}'.format(old=old, new=new))

    # actual renaming
    if input('Start batch rename? (y/n) ') == 'y':
        for old, new in zip(files_list, new_names):
            os.rename(old, new)
        print('Done.')
    else:
        print('Aborted.')
