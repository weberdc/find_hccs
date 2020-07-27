#!/bin/env python3

import csv
import os.path
import shutil
import sys
import utils

from os import path

# Sorts the rows in a CSV output of raw_to_csv.py into timestamp order.
# Useful when you've created the CSV from an input file not in timestamp order
# (e.g., the RU-IRA tweets)

if __name__=='__main__':

    print('Starting: %s' % utils.now_str())

    in_f = sys.argv[1]
    backup = '%s.bkp' % in_f

    i = 1
    backup_base = backup
    while path.exists(backup):
        backup = '%s%d' % (backup_base, i)
        i += 1

    print('Backing up to %s' % backup)
    shutil.copyfile(in_f, backup)

    print('Reading in %s' % backup)
    rows = []
    with open(backup, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        field_names = reader.fieldnames
        for r in reader:
            rows.append(r)

    print('Sorting...')
    rows = sorted(rows, key=lambda r: r['timestamp'])

    print('Writing back to %s' % in_f)
    with open(in_f, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()

        for r in rows:
            writer.writerow(r)

    print('Done at %s' % utils.now_str())
