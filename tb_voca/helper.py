# -*- coding: utf-8 -*-

import os
import csv

from os.path import join
from .word import Word


def print_file_list(path, verbose=True):
    file_list = list()

    idx = 1
    for root_path, dirs, files in os.walk(path):
        depth = root_path.replace(path, '').count(os.sep)
        indent = '   ' * 1 * depth
        if verbose:
            print('%s%s/' % (indent, root_path))
        child_indent = '   ' * 1 * (depth + 1)
        for f in files:
            if verbose:
                print('%s- %d. %s' % (child_indent, idx, f))
            file_list.append(join(root_path, f))
            idx += 1

    return file_list


def read_csv(file):
    file = open(file, 'r', encoding='utf-8')
    word_list = []
    reader = csv.reader(file)
    for line in reader:
        word_param = {}
        try:
            word_param['word'] = line[0]
        except IndexError:
            word_param['word'] = ''

        try:
            word_param['e_mean'] = line[1]
        except IndexError:
            word_param['e_mean'] = ''

        try:
            word_param['k_mean'] = line[2]
        except IndexError:
            word_param['k_mean'] = ''

        try:
            word_param['sentence'] = line[3]
        except IndexError:
            word_param['sentence'] = ''
        word_list.append(Word(word=word_param['word'],
                              e_mean=word_param['e_mean'],
                              k_mean=word_param['k_mean'],
                              sentence=word_param['sentence']))
    file.close()
    return word_list
