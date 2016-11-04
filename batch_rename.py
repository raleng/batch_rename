#!/usr/bin/python3
import begin
import getpass
import math
import os
from itertools import compress
from os.path import isfile, join


def get_sorted_file_names():
    """ Get files names of CWD and sort them.

    Is able to handle reasonable sorting of
    NAME2.jpg
    NAME12.jpg
    """
    cwd = os.getcwd()
    print('Working Dir: {}'.format(cwd))

    # just a little sanity check
    if cwd == '/home/{}'.format(getpass.getuser()):
        print('Ehm, no?')
        exit()

    # get only files in directory and sort
    files_list = [f for f in os.listdir(cwd) if isfile(join(cwd, f))]

    lengths = sorted(list({len(name) for name in files_list}))
    for l in lengths:
        mask = [1 if len(n) == l else 0 for n in files_list]
        partial_names = sorted(list(compress(files_list, mask)))
        yield from partial_names


def do_renaming(old_names, new_names):
    """ Renames the files; does a dry run first """
    # renaming dry run
    for old, new in zip(old_names, new_names):
        print('{old} --> {new}'.format(old=old, new=new))

    # actual renaming
    if input('Start batch rename? (y/n) ') == 'y':
        for old, new in zip(old_names, new_names):
            os.rename(old, new)
        print('Done.')
    else:
        print('Aborted.')


def rename_with_counter(files_list, usr_str, lead_zeros):
    """ Yields new names ending with correct counter values. """
    for count, file_name in enumerate(files_list, start=1):
        file_count = str(count).zfill(lead_zeros)
        file_ext = file_name.split('.')[-1]
        new = '{usr}{num}.{ext}'.format(usr=usr_str, num=file_count, ext=file_ext)
        yield new


def rename_with_replace(files_list, old, new):
    """ Yields new names with replaced string parts. """
    for file_name in files_list:
        yield file_name.replace(old, new)


@begin.subcommand
def counter(user_str, *, lead_zeros=1):
    """ Renames all files with correct counter at the end. """
    files_list = list(get_sorted_file_names())
    # check how many leading zeros are necessary
    lead_zeros = max(int(math.log10(len(files_list))) + 1, lead_zeros)

    new_names = list(rename_with_counter(files_list, user_str, lead_zeros))
    do_renaming(files_list, new_names)


@begin.subcommand
def replace(old_str, new_str):
    """ Renames all files with replaced string parts. """
    files_list = list(get_sorted_file_names())
    new_names = list(rename_with_replace(files_list, old_str, new_str))
    do_renaming(files_list, new_names)


@begin.start(auto_convert=True)
def main():
    """ Batch renaming of all files in current directory. """
    pass
