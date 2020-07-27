#!/usr/bin/env python3

from __future__ import print_function

import csv
import sys

from argparse import ArgumentParser

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'cut_csv.py -i <in_file>.csv -o <out_file>.csv [--column-indexes 2,3,1] [--column-names "col 1",col3,"col 2"]'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default='-',
            dest='in_file',
            help='Big CSV file with or without headers (use column indexes without headers)'
        )
        self.parser.add_argument(
            '-o',
            default='-',
            dest='out_file',
            help='Extract columns of the big CSV'
        )
        self.parser.add_argument(
            '-f', '--column-indexes',
            # default='',
            dest='col_idxs',
            help='Indexes of columns to extract (starts at 1)'
        )
        self.parser.add_argument(
            '-d', '--delimiter',
            default=',',
            dest='delimiter',
            help='Delimiter between fields (default is ",")'
        )
        self.parser.add_argument(
            '--output-delimiter',
            default=None,
            dest='output_delimiter',
            help='The output delimiter (the default is to use the input delimiter)'
        )
        self.parser.add_argument(
            '--column-names',
            # default='',
            dest='col_names',
            help='Names of columns to extract (case-sensitive)'
        )
        self.parser.add_argument(
            '-v', '--verbose',
            dest='verbose',
            action='store_true',
            default=False,
            help='Verbose logging (default: False)'
        )

    def parse(self, args=None):
        return self.parser.parse_args(args)


def process_opts(opts):
    in_file = opts.in_file
    out_file = opts.out_file
    col_idxs = opts.col_idxs.split(',') if opts.col_idxs else []
    col_names = opts.col_names.split(',') if opts.col_names else []
    delim = opts.delimiter
    out_delim = opts.output_delimiter if opts.output_delimiter else delim

    # convert to ints
    col_idxs = list(map(lambda i: int(i), col_idxs))

    # strip quotes
    for i in range(len(col_names)):
        if col_names[i][0] == '"': col_names[i] = col_names[1:-1]

    log('In:       %s' % in_file)
    log('Out:      %s' % out_file)
    log('Columns:  %s' % col_names)
    log('Columns:  %s' % col_idxs)
    log('Delim.:   %s' % delim)
    log('Out del.: %s' % delim)

    return (in_file, out_file, col_idxs, col_names, delim, out_delim)


def create_writer(out_f, col_names, delim=','):
    writer = None
    if col_names:
        writer = csv.DictWriter(out_f, fieldnames=col_names)
        writer.writeheader()
    else:
        writer = csv.writer(out_f, delimiter=delim, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    return writer


def create_reader(in_f, col_names, delim):
    if col_names:
        return csv.DictReader(in_f)
    else:
        return csv.reader(in_f, delimiter=delim, quotechar='"')


def write_row(r, writer, col_names, col_idxs):
    def safe_get(l, idx):
        if idx > -1 and idx < len(l):
            return l[idx]
        else:
            return ''
    if col_names:
        out_r = dict([(col_name, r[col_name]) for col_name in col_names])
        writer.writerow(out_r)
    else:
        out_r = [safe_get(r, i-1) for i in col_idxs]
        writer.writerow(out_r)


def log_update(line_count):
    if DEBUG:
        line_count += 1
        if line_count % 100 == 0: eprint('.', end='')
        if line_count % 5000 == 0: eprint(' %8d' % line_count)
    return line_count


def eprint(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


DEBUG=False
def log(msg):
    if DEBUG: eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    (in_file, out_file, col_idxs, col_names, in_delim, out_delim) = process_opts(opts)

    try:
        if out_file == '-':
            out_f = sys.stdout
        else:
            out_f = open(out_file, mode='w', newline='\n', encoding='utf-8')

        writer = create_writer(out_f, col_names, out_delim)

        if in_file == '-':
            in_f = sys.stdin
        else:
            in_f = open(in_file, 'r', newline='', encoding='utf-8')

        reader = create_reader(in_f, col_names, in_delim)

        line_count = 0
        for r in reader:
            try:
                write_row(r, writer, col_names, col_idxs)
            except IOError:
                log('Someone hit Ctrl-C')
                sys.exit()

            line_count = log_update(line_count)

    finally:
        if in_file != '-' and in_f:
            in_f.close()
        if out_file != '_' and out_f:
            out_f.close()

    log('\nProcessed %d rows' % line_count)
