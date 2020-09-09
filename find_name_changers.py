#!/usr/bin/env python3

import gzip
import json
import sys
import utils

from argparse import ArgumentParser

# Finds accounts which changed their screen names and when

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'find_name_changers.py -i tweets.json[.gz] -o <out>.json'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default=None,
            required=True,
            dest='tweets_file',
            help='A file of tweets, possibly gzipped'
        )
        self.parser.add_argument(
            '-o',
            default=None,
            required=True,
            dest='out_file',
            help='A JSON file of the name changers, their profiles and activity'
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

DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    tweets_file = opts.tweets_file
    out_file = opts.out_file

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    screen_names = {}  # id : screen_name
    offenders = set()
    in_f = gzip.open(tweets_file, 'rt', encoding='utf-8') if tweets_file[-1] in 'zZ' else open(tweets_file, 'r', encoding='utf-8')
    line_count = 0
    tweet_count = 0
    for l in in_f:
        tweet_count += 1
        line_count = utils.log_row_count(line_count, DEBUG)
        t = json.loads(l)
        uid = t['user']['id_str']
        if uid not in offenders:
            if uid in screen_names:
                if screen_names[uid] != t['user']['screen_name']:
                    offenders.add(uid)
            else:
                screen_names[uid] = t['user']['screen_name']

    log('Found %d accounts, %d offenders in %d tweets' % (len(screen_names), len(offenders), tweet_count))

    log('Processing offenders')
    profiles = {} # id : { profile: ..., activity: [(ts, name)], changer: boolean }
    line_count = 0
    tweet_count = 0
    in_f.seek(0)  # reset file reading cursor to start of file
    for l in in_f:
        tweet_count += 1
        line_count = utils.log_row_count(line_count, DEBUG)
        t = json.loads(l)
        uid = t['user']['id_str']
        if uid in offenders:
            tweet_count += 1
            if uid not in profiles:
                profiles[uid] = { 'tweets' : [], 'names_at_time' : [] }
            pdata = profiles[uid]
            t['dcw_ts'] = utils.extract_ts_s(t['created_at'])
            pdata['tweets'].append(t)
            pdata['names_at_time'].append( (t['dcw_ts'], t['user']['screen_name']) )
    log('Extracted %d tweets by %d offenders' % (tweet_count, len(offenders)))

    with open(out_file, 'w', encoding='utf-8') as out_f:
        for uid in profiles:
            out_f.write(json.dumps(profiles[uid]))
            out_f.write('\n')

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
