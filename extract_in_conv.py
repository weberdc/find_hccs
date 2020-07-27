#!/usr/bin/env python3

import csv
import gzip
import json
import re
import sys
import utils

from argparse import ArgumentParser

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'extract_in_conv.py -i tweets_file.[json[l|.gz]|csv] -o in_converation.csv [--ira]'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default='-',
            dest='tweets_file',
            help='File of tweets, if relevant, one tweet per line ("-" for stdin, end filename with z for gzip)'
        )
        self.parser.add_argument(
            '-o',
            default='-',
            dest='csv_file',
            help='Relevant parts of tweets as CSV'
        )
        self.parser.add_argument(
            '--ira',
            dest='ira',
            action='store_true',
            default=False,
            help='Expect Twitter\'s IRA dataset (default: False)'
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


def write_header(f, topic):
    if topic == 'RETWEET':
        f.write('timestamp,source,target,interaction,rt_id,ot_id\n')
    elif topic in list(set(TOPICS) - set(['RETWEET', 'MENTION'])):
        f.write('timestamp,source,target,interaction,t_id\n')
    elif topic == 'MENTION':
        f.write('timestamp,source,target,interaction,t_id,mentioned_screen_name\n')


# def write_url_row(csv_f, topic, url, ts, source, t_id):
#     if 'http' not in url:
#         utils.eprint('URL in tweet [%s] is invalid: %s' % (t_id, url))
#         return
#
#     if topic == 'URL' and not TWEET_URL_REGEX.match(url):
#         csv_f.writerow([ts, source, url, 'URL', t_id])
#     elif topic == 'ALL_URL':
#         csv_f.writerow([ts, source, url, 'POST_URL', t_id])
#     elif topic == 'DOMAIN' and not TWEET_URL_REGEX.match(url):
#         csv_f.writerow([ts, source, utils.extract_domain(url), 'DOMAIN', t_id])
#     elif topic == 'ALL_DOMAIN':
#         csv_f.writerow([ts, source, utils.extract_domain(url), 'ALL_DOMAIN', t_id])
#     elif topic == 'POST_URL' and not TWEET_URL_REGEX.match(url):
#         post_url = url[:url.index('?')] if '?' in url else url
#         csv_f.writerow([ts, source, post_url, 'POST_URL', t_id])


def parse_tweet_obj(t, tweets):
    REPLY_KEY = 'in_reply_to_status_id_str'
    is_a_reply = REPLY_KEY in t and t[REPLY_KEY]

    t_id = t['id_str']
    tweets[t_id] = {
        'timestamp' : utils.extract_ts_s(t['created_at']),
        'reply_id' : t_id,
        'source' : utils.get_uid(t),
        'interaction' : 'IN_CONV',
        'target' : None,
        'ot_id' : None,
        'in_reply_to_t_id' : t[REPLY_KEY] if is_a_reply else None,
        'in_reply_to_u_id' : t['in_reply_to_user_id_str'] if is_a_reply else None
    }


def parse_ira_tweet(t, tweets):
    REPLY_KEY = 'in_reply_to_tweetid'
    is_a_reply = REPLY_KEY in t and t[REPLY_KEY]

    t_id = t['tweetid']
    tweets[t_id] = {
        'timestamp' : utils.extract_ts_s(t['tweet_time'], fmt=utils.IRA_TS_FORMAT),
        'reply_id' : t_id,
        'source' : t['userid'],
        'interaction' : 'IN_CONV',
        'target' : None,
        'ot_id' : None,
        'in_reply_to_t_id' : t[REPLY_KEY] if is_a_reply else None,
        'in_reply_to_u_id' : t['in_reply_to_userid'] if is_a_reply else None
    }


def follow_chain(t_id, tweets):
    # print('follow_chain(%s)' % t_id)
    t = tweets[t_id]
    if t['ot_id']:
        return

    ancestor_tweet_id = t['in_reply_to_t_id']
    # print('  ancestor_tweet_id: %s (known? %s)' % (ancestor_tweet_id, ancestor_tweet_id in tweets))
    if ancestor_tweet_id not in tweets:
        # next tweet back is not in the corpus
        t['target'] = t['in_reply_to_u_id']
        t['ot_id'] = ancestor_tweet_id
        return

    if not tweets[ancestor_tweet_id]['ot_id']:
        # next tweet back hasn't been processed yet
        follow_chain(ancestor_tweet_id, tweets)
    # ancestor should be filled out by this point
    t['target'] = tweets[ancestor_tweet_id]['target']
    t['ot_id'] = tweets[ancestor_tweet_id]['ot_id']


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    tweets_file = opts.tweets_file
    csv_file = opts.csv_file
    # topic = opts.topic
    ira = opts.ira

    if tweets_file[-1] in 'zZ':
        in_f = gzip.open(tweets_file, 'rt', encoding='utf-8')
    else:
        in_f = open(tweets_file, 'r', encoding='utf-8')

    line_count = 0
    tweets = {}  # tweet ID : { ts, tweet ID, conv_root ID, replier ID, conv_root author ID }
    if ira:
        csv_reader = csv.DictReader(in_f)
        for row in csv_reader:
            line_count = utils.log_row_count(line_count, DEBUG)
            parse_ira_tweet(row, tweets)
    else:
        for l in in_f:
            line_count = utils.log_row_count(line_count, DEBUG)
            t = json.loads(l)
            parse_tweet_obj(t, tweets)

    log('\nFound %d replies, building chains...' % len(tweets))

    # TODO how to ignore when one of the participants posted the original tweet? They will be over-represented

    for t_id in tweets:
        follow_chain(t_id, tweets)

    # strip un-replied to tweets
    to_keep = set()
    for t_id in tweets:
        t = tweets[t_id]
        if t['in_reply_to_t_id'] != None:
            to_keep.add(t_id)
            # to_keep.add(t['in_reply_to_t_id'])
    log('Only keeping %d tweets' % len(to_keep))
    for to_remove in (tweets.keys() - to_keep):
        del tweets[to_remove]

    with open(csv_file, mode='w', newline='\n', encoding='utf-8') as out_f:
        # write_header(out_f, topic)
        FIELD_NAMES = ['timestamp','source','target','interaction','reply_id','ot_id']
        out_f.write('%s\n' % ','.join(FIELD_NAMES))
        csv_writer = csv.DictWriter(out_f, fieldnames=FIELD_NAMES, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        count = 0
        for t_id in tweets:
            t = tweets[t_id]
            if not t['target'] or t['source'] == t['target']: continue
            t['ot_id'] = t['in_reply_to_t_id']  # keep transitive link
            del t['in_reply_to_t_id']
            del t['in_reply_to_u_id']
            count += 1
            csv_writer.writerow(t)
        log('Wrote %d records' % count)

    log('DONE')
