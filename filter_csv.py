#!/usr/bin/env python

from argparse import ArgumentParser

import os
import sys
import utils

# Keep or remove rows from a text file based on keywords

class Options:
    def __init__(self):
        self.usage = '%s [options] <term> [<term>]*' % os.path.basename(__file__)
        self.parser = ArgumentParser(usage=self.usage, conflict_handler='resolve')
        self.parser.add_argument(
            'terms',
            metavar='terms',
            type=str,
            nargs='*',
            help='Term to keep or remove'
        )
        self.parser.add_argument(
            '-x', '--exclude',
            action='store_true',
            default=False,
            dest='exclude',
            help='Exclude rows with these terms, rather than keeping them (default: False)'
        )
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            default=False,
            dest='verbose',
            help='Turn on verbose logging (default: False)'
        )
        self.parser.add_argument(
            '-i',
            dest='in_file',
            default='',
            required=True,
            help='File to read from.'
        )
        self.parser.add_argument(
            '-o',
            dest='out_file',
            default='',
            required=True,
            help='File to write output to.'
        )

    def parse(self, args=None):
        return self.parser.parse_args(args)


DEBUG=False
def log(msg=None):
    if DEBUG: utils.logts(msg) if msg else utils.eprint()


if __name__=='__main__':
    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    STARTING_TIME = utils.now_str()
    log('Starting at %s' % STARTING_TIME)

    in_file = opts.in_file
    out_file = opts.out_file
    terms = opts.terms
    exclude = opts.exclude
    include = not exclude

    if include:
        print('Not yet implemented')
        sys.exit()

    line_count = 0
    with open(out_file, 'w', encoding='utf-8') as out_f:
        with open(in_file, 'r', encoding='utf-8') as in_f:
            for l in in_f:
                skip_line = False
                line_count = utils.log_row_count(line_count, DEBUG)
                for t in terms:
                    if (exclude and t in l):  # or (include and t not in l):
                        skip_line = True
                        break
                if not skip_line:
                    out_f.write(l)
    log('')

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
