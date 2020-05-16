#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

__author__ = 'Charles'

OUTPUT_FILE = 'G268_fpkm_all.txt'

ROOT_PATH = '/projects/GaoLab'
FOLDERS = ['G268-1_trimmed', 'G268-2_trimmed']
FILE_NAME = 'genes.fpkm_tracking'


def main():
    big_table = {}
    summary = {}
    cell_list = []
    for fd in FOLDERS:
        pfd = os.path.join(ROOT_PATH, fd)
        list_dirs = os.walk(pfd)
        for root, dirs, files in list_dirs:
            for d in dirs:
                big_table[d] = {}
                summary[d] = {}
                cell_list.append(d)
                path = os.path.join(pfd, d, FILE_NAME)
                with open(path, "r") as fp:
                    is_first_line = True
                    for line in fp.readlines():
                        if is_first_line:
                            is_first_line = False
                            continue
                        lns = line.split()
                        big_table[d][lns[0]] = float(lns[9])
                summary_file = os.path.join(pfd, d, "align_summary.txt")
                with open(summary_file, "r") as fp:
                    for line in fp.readlines():
                        l = line.strip().split()
                        if l[0] == "Input":
                            summary[d]["Input"] = int(l[2])
                        elif l[0] == "Mapped":
                            summary[d]["Mapped"] = int(l[2])
    gene_list = big_table[cell_list[0]].keys()

    all_reads_file = OUTPUT_FILE
    with open(all_reads_file, 'w') as fp:
        first_line = ''
        for c in cell_list:
            first_line += '\t' + c
        first_line += '\n'
        fp.write(first_line)

        for g in gene_list:
            line = g
            for c in cell_list:
                line += ('\t%d' % big_table[c][g])
            line += '\n'
            fp.write(line)


if __name__ == '__main__':
    main()
