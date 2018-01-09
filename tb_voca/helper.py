# -*- coding: utf-8 -*-

import os

from os.path import join


def print_file_list(path):
    file_list = list()

    idx = 1
    for root_path, dirs, files in os.walk(path):
        depth = root_path.replace(path, '').count(os.sep)
        indent = '\t' * 1 * depth
        print('%s%s/' % (indent, root_path))
        child_indent = '\t' * 1 * (depth + 1)
        for f in files:
            print('%sㄴ %d. %s' % (child_indent, idx, f))
            file_list.append(join(root_path, f))
            idx += 1

    return file_list
