#!/usr/bin/env python3

import csv
import gzip
import json
import math
import networkx as nx
import re
import sys
import utils

from argparse import ArgumentParser

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'extract_in_conv_to_lcn.py -i tweets_file.[json[l|.gz]|csv] -o <in_conv> [--ira] [--lcn]'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default='-',
            dest='tweets_file',
            help='File of tweets, if relevant, one tweet per line ("-" for stdin, end filename with z for gzip)'
        )
        self.parser.add_argument(
            '-o',
            required=True,#default='-',
            dest='out_file',
            help='The derived CSV or LCN'
        )
        self.parser.add_argument(
            '-w', '--window',
            default='15m',
            dest='window_str',
            help='Window size with unit [smhd], e.g., 15m = 15 minutes, 10s = 10 seconds, 24h = 24 hours, 7d = 7 days'
        )
        self.parser.add_argument(
            '--ira',
            dest='ira',
            action='store_true',
            default=False,
            help='Expect Twitter\'s IRA dataset (default: False)'
        )
        self.parser.add_argument(
            '--lcn',
            dest='lcn',
            action='store_true',
            default=False,
            help='Create a LCN GraphML directly, avoiding find_behaviour (default: False)'
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


# def write_header(f, topic):
#     if topic == 'RETWEET':
#         f.write('timestamp,source,target,interaction,rt_id,ot_id\n')
#     elif topic in list(set(TOPICS) - set(['RETWEET', 'MENTION'])):
#         f.write('timestamp,source,target,interaction,t_id\n')
#     elif topic == 'MENTION':
#         f.write('timestamp,source,target,interaction,t_id,mentioned_screen_name\n')


def parse_tweet_obj(t, tweets):
    REPLY_KEY = 'in_reply_to_status_id_str'
    is_a_reply = REPLY_KEY in t and t[REPLY_KEY]

    t_id = t['id_str']
    tweets[t_id] = {
        'timestamp' : utils.extract_ts_s(t['created_at']),
        'reply_tid' : t_id,
        'source_uid' : utils.get_uid(t),
        'source_sn' : t['user']['screen_name'],
        'interaction' : 'IN_CONV',
        'target_tid' : None,
        'target_uid' : None,
        'orig_tid' : None,
        'in_reply_to_tid' : t[REPLY_KEY] if is_a_reply else None,
        'in_reply_to_uid' : t['in_reply_to_user_id_str'] if is_a_reply else None,
        'raw': t,
        'type': 'TWITTER'
    }


def parse_ira_tweet(t, tweets):
    REPLY_KEY = 'in_reply_to_tweetid'
    is_a_reply = REPLY_KEY in t and t[REPLY_KEY]

    t_id = t['tweetid']
    tweets[t_id] = {
        'timestamp' : utils.extract_ts_s(t['tweet_time'], fmt=utils.IRA_TS_FORMAT),
        'reply_tid' : t_id,
        'source_uid' : t['userid'],
        'source_sn' : t['user_screen_name'],
        'interaction' : 'IN_CONV',
        'target_tid' : None,
        'target_uid' : None,
        'orig_tid' : None,
        'in_reply_to_tid' : t[REPLY_KEY] if is_a_reply else None,
        'in_reply_to_uid' : t['in_reply_to_userid'] if is_a_reply else None,
        'raw' : t,
        'type': 'IRA'
    }


def follow_chain(t_id, tweets):
    # print('follow_chain(%s)' % t_id)
    t = tweets[t_id]
    if t['orig_tid']:  # already followed this path
        return

    ancestor_tweet_id = t['in_reply_to_tid']
    # print('  ancestor_tweet_id: %s (known? %s)' % (ancestor_tweet_id, ancestor_tweet_id in tweets))

    if ancestor_tweet_id in tweets:
        follow_chain(ancestor_tweet_id, tweets)
        # now populate current tweet with ancestor tweet details
        t['target_tid'] = tweets[ancestor_tweet_id]['target_tid']
        t['target_uid'] = tweets[ancestor_tweet_id]['target_uid']
        t['orig_tid'] = tweets[ancestor_tweet_id]['orig_tid']

    else:
        # populate current tweet with what we have
        t['target_tid'] = t['in_reply_to_tid']
        t['target_uid'] = t['in_reply_to_uid']  #None
        t['orig_tid'] = ancestor_tweet_id


    # if ancestor_tweet_id not in tweets:
    #     # next tweet back is not in the corpus
    #     t['target_tid'] = t['in_reply_to_tid']
    #     t['target_uid'] = t['in_reply_to_uid']  #None
    #     t['orig_tid'] = ancestor_tweet_id
    #     return
    #
    # if not tweets[ancestor_tweet_id]['orig_tid']:
    #     # next tweet back hasn't been processed yet
    #     follow_chain(ancestor_tweet_id, tweets)
    # # ancestor should be filled out by this point
    # t['target_tid'] = tweets[ancestor_tweet_id]['target_tid']
    # t['target_uid'] = tweets[ancestor_tweet_id]['target_uid']
    # t['orig_tid'] = tweets[ancestor_tweet_id]['orig_tid']


def extract_csv_row(t):
    def safe(v): return v if v else ''
    row = ['%d' % t['timestamp'], safe(t['source_uid']), safe(t['target_uid']), 'IN_CONV', safe(t['reply_tid']), safe(t['target_tid'])]
    # if None in row:
    #     print(json.dumps(t, sort_keys=True, indent=4))
    #     print(row)
    #     sys.exit()
    return row


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    tweets_file = opts.tweets_file
    out_file = opts.out_file
    # topic = opts.topic
    ira = opts.ira
    window_s = utils.parse_window_cli_arg(opts.window_str)

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

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

    post_counts = {}
    for t in tweets.values():
        if t['source_uid'] not in post_counts:
            post_counts[t['source_uid']] = 0.0
        post_counts[t['source_uid']] += 1.0

    log('')
    log('Found %d replies' % len(tweets))

    # collate the screen names we know
    log('Collecting known screen names')
    known_screen_names = { t['source_uid'] : t['source_sn'] for t in tweets.values() }

    # TODO how to ignore when one of the participants posted the original tweet? They will be over-represented

    log('Building chains...')
    for t_id in tweets:
        # flesh out the chain info
        follow_chain(t_id, tweets)

    # strip un-replied to tweets
    to_keep = {}
    for t_id in tweets:
        t = tweets[t_id]
        if t['target_tid']:  # t['in_reply_to_tid'] != None:
            to_keep[t_id] = t
            # to_keep.add(t_id)
            # to_keep.add(t['in_reply_to_t_id'])
    log('Only keeping %d tweets' % len(to_keep))
    tweets = to_keep
    # for to_remove in (tweets.keys() - to_keep):
    #     del tweets[to_remove]

    if not opts.lcn:
        int_list = list(filter(lambda t: t[2], map(extract_csv_row, tweets.values())))
        int_list.sort(key=lambda t: t[0])  # timestamp column
        log('Writing to %s' % out_file)
        with open(out_file, 'w', encoding='utf-8') as out_f:
            # ts, src_uid, tgt_uid, IN_CONV, reply_tid, orig_tid
            out_f.write('timestamp,source,target,interaction,reply_id,ot_id\n')
            for int_i in int_list:
                # print(int_i)
                # print(','.join(int_i))
                out_f.write('%s\n' % ','.join(int_i))
    else:
        log('Building inconv LCN')
        g = nx.Graph()
        ts = list(tweets.values())
        ts.sort(key=lambda t: t['timestamp'])
        for i in range(len(ts) - 1):
            for j in range(i+1, len(ts)):
                line_count = utils.log_row_count(line_count, DEBUG, 1000000, 50000000)
                t1 = ts[i]
                t2 = ts[j]  # always later than t1
                same_target = t1['target_tid'] == t2['target_tid']
                diff_source = t1['source_uid'] != t2['source_uid']
                within_cooee = window_s - (t2['timestamp'] - t1['timestamp']) >= 0
                if t1['target_tid'] and t1['source_uid'] and t2['source_uid'] and same_target and diff_source and within_cooee:
                    src = t1['source_uid']
                    tgt = t2['source_uid']
                    if src not in g:
                        g.add_node(src, label=src, post_count=post_counts[src], screen_name=known_screen_names.get(src, ''))
                    if tgt not in g:
                        g.add_node(tgt, label=tgt, post_count=post_counts[tgt], screen_name=known_screen_names.get(tgt, ''))
                    if not g.has_edge(src, tgt):
                        g.add_edge(src, tgt, interaction=t['interaction'], weight=1.0, reasons=[t1['target_tid']])
                    else:
                        g[src][tgt]['weight'] += 1.0
                        g[src][tgt]['reasons'].append(t1['target_tid'])

        for u, v, r in g.edges(data='reasons'):
            g[u][v]['reasons'] = ','.join(r)  # json.dumps(r)  # make serialisable

        log('Writing to %s' % out_file)
        nx.write_graphml(g, out_file)

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
