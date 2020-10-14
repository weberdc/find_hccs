#!/usr/bin/env python3

import gzip
import json
import sys
import time
import utils

from argparse import ArgumentParser
from datetime import datetime


class Options:
    def __init__(self):
        self._init_parser('filter_tweets_by_author.py -t|--tweets_file <file of tweets> -a|--authors-file <author_id_file> [--count] [--pretty]')

    def _init_parser(self, usage):
        self.parser = ArgumentParser(usage=usage, conflict_handler='resolve')
        self.parser.add_argument(
            '-t', '-i', '--tweets-file',
            default='-',
            required=True,
            dest='tweets_file',
            help='Tweets file (default: -)'
        )
        self.parser.add_argument(
            '-o', '--out-file',
            default='-',
            dest='out_file',
            help='File to write matching tweets to'
        )
        self.parser.add_argument(
            '-a', '--authors-file',
            default=None,
            required=True,
            dest='authors_file',
            help='Authors file (default: "")'
        )
        self.parser.add_argument(
            '-c', '--count',
            action='store_true',
            default=False,
            dest='count',
            help='Just count the tweets (default: False)'
        )
        self.parser.add_argument(
            '--pretty',
            action='store_true',
            default=False,
            dest='pretty',
            help='Pretty print relevant content of matching tweets to stdout (default: False, output full JSON)'
        )
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            default=False,
            dest='verbose',
            help='Turn on verbose logging (default: False)'
        )


    def parse(self, args=None):
        return self.parser.parse_args(args)


TWITTER_TS_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'  #Tue Apr 26 08:57:55 +0000 2011

def parse_ts(ts_str, fmt=TWITTER_TS_FORMAT):
    time_struct = time.strptime(ts_str, fmt)
    return datetime.fromtimestamp(time.mktime(time_struct))


def process_lines(in_f, action):
    match_count = 0
    count = 0
    for l in f:
        count += 1
        if DEBUG:
            if count % 10000 == 0: log('%8d' % count)
        t = json.loads(l)
        if t['user']['id_str'] in ids_of_interest:
            action(l) #o.write(l)
            match_count += 1
    return (count, match_count)


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose
    log('Started %s' % datetime.now())

    ids_of_interest = utils.fetch_lines(opts.authors_file) if opts.authors_file else opts.i_files
    # strip quotes if they're present
    ids_of_interest = ids_of_interest if ids_of_interest[0][0] != '"' else [id[1:-1] for id in ids_of_interest]
    if ',' in ids_of_interest[0]:
        ids_of_interest = list(map(lambda s: s.split(',')[0], ids_of_interest))
    tweets_file = opts.tweets_file
    # pretty = opts.pretty

    def my_open_file(fn, gz=False):
        if gz:
            return gzip.open(fn, 'rt')  # needs to be read as 't' (text) but 'b' works elsewhere
        else:
            return open(fn, 'r', encoding='utf-8')

    count = 0
    match_count = 0
    with my_open_file(tweets_file, tweets_file[-1] in 'zZ') as f:
        if opts.count:
            (count, match_count) = process_lines(f, lambda l: None)
        else:
            with open(opts.out_file, 'w', encoding='utf-8') as o:
                (count, match_count) = process_lines(f, lambda l: o.write(l))

        # with open(opts.out_file, 'w', encoding='utf-8') as o:
        #     for l in f:
        #         count += 1
        #         if DEBUG:
        #             if count % 10000 == 0: log('%8d' % count)
        #         t = json.loads(l)
        #         if t['user']['id_str'] in ids_of_interest:
        #             o.write(l)
        #             match_count += 1

    utils.eprint('all lines: %d' % count)
    utils.eprint('matching:  %d' % match_count)

    log('Ended %s' % datetime.now())
