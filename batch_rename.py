#!/usr/bin/env python3
import begin
import getpass
import math
import os
import re
from os.path import isfile


def try_int(string):
    try:
        return int(string)
    except:
        return string


def alphanum_key(string):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [try_int(c) for c in re.split('([0-9]+)', string)]


def get_sorted_file_names():
    """ Get files names of CWD and sort them.

    Is able to handle reasonable sorting of
    NAME2.jpg
    NAME12.jpg
    """
    cwd = os.getcwd()
    print(f'Working Dir: {cwd}')

    # just a little sanity check
    if cwd == '/home/{}'.format(getpass.getuser()):
        print('Ehm, no?')
        exit()

    # get only files in directory and sort
    files_list = [f for f in os.listdir(cwd) if isfile(f)]
    files_list.sort(key=alphanum_key)

    yield from files_list


def do_renaming(old_names, new_names):
    """ Renames the files; does a dry run first """
    # renaming dry run
    for old, new in zip(old_names, new_names):
        if old == new:
            print(f'No change to: {old}')
        else:
            print(f'{old} --> {new}')

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
        new = f'{usr_str}{file_count}.{file_ext}'
        yield new


def rename_with_replace(files_list, old, new, regex):
    """ Yields new names with replaced string parts. """
    for file_name in files_list:
        if regex:
            try:
                old_replace = re.findall(old, file_name)[0]
            except IndexError:
                continue
        else:
            old_replace = old
        new_name = file_name.replace(old_replace, new)
        if not file_name == new_name:
            yield file_name, new_name


@begin.subcommand
def counter(user_str, *, lead_zeros=1):
    """ Renames all files with correct counter at the end. """
    files_list = list(get_sorted_file_names())
    # check how many leading zeros are necessary
    lead_zeros = max(int(math.log10(len(files_list))) + 1, int(lead_zeros))

    new_names = list(rename_with_counter(files_list, user_str, lead_zeros))
    do_renaming(files_list, new_names)


@begin.subcommand
def replace(old_str, new_str, *, regex=False):
    """ Renames all files with replaced string parts. """
    files_list = list(get_sorted_file_names())
    rwr = list(rename_with_replace(files_list, old_str, new_str, regex))
    if len(rwr) != 0:
        files_list, new_names = map(list, zip(rwr))
        do_renaming(files_list, new_names)


@begin.start
def main():
    """ Batch renaming of all files in current directory. """
    pass
