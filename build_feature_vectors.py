#!/usr/bin/env python3

import csv
import json
import networkx as nx
import os
import statistics
import sys
import utils

from argparse import ArgumentParser
from networkx.algorithms.approximation.clustering_coefficient import average_clustering

# Builds feature vectors for HCC members and their groupings as input to the
# classifiers for validation

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'build_feature_vectors.py --hccs <hccs>.graphml --analysis <hcc_analysis>.json'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '--hccs',
            default=None,
            required=True,
            dest='hccs_file',
            help='An HCCs file (graphml)'
        )
        self.parser.add_argument(
            '--analysis',
            default=None,
            required=True,
            dest='analysis_file',
            help='An HCC analysis file (JSON)'
        )
        self.parser.add_argument(
            '--tweets',
            default=None,
            required=True,
            dest='tweets_file',
            help='The corpus of tweets (JSON) (may be gzipped)'
        )
        self.parser.add_argument(
            '-l', '--label',
            dest='label',
            default=None,
            help='Label to apply to these feature vectors (default: False)'
        )
        self.parser.add_argument(
            '-o',
            dest='out_file',
            default=None,
            help='Output for HCCs specifically (default: False)'
        )
        self.parser.add_argument(
            '--random',
            dest='random',
            action='store_true',
            default=False,
            help='Provided analysis file is for the randomised HCCs (default: False)'
        )
        self.parser.add_argument(
            '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help='Dry run, writes no files (default: False)'
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


def build_f_vecs_for(hcc_info, hcc, accts, corpus_duration_d, f_vecs):
    V = hcc.nodes
    E = hcc.edges

    all_tss = []
    tweet_tss = {}  # acct_id : tweet timestamps
    for t in hcc_info['tweets']:
        u_id = t['u_id']
        t_ts = t['t_ts']
        all_tss.append(t_ts)
        if u_id not in tweet_tss:
            tweet_tss[u_id] = [t_ts]
        else:
            tweet_tss[u_id].append(t_ts)

    all_tss.sort()
    for u in tweet_tss:
        tweet_tss[u].sort()

    a_vecs = {}
    for u_id in hcc_info['users']:
        user = hcc_info['users'][u_id]
        # account features
        acct = accts[u_id]
        age_d = s_to_d(max(tweet_tss[u_id]) - s_to_ts(acct['created_at']))
        a_iatss = interarrival_times(tweet_tss[u_id])
        a_vec = {}
        a_vec['A_age'] = age_d
        a_vec['A_followers'] = acct['followers_count']
        a_vec['A_friends'] = acct['friends_count']
        a_vec['A_reputation'] = a_vec['A_friends'] / float(a_vec['A_friends']+a_vec['A_followers'])
        a_vec['A_lifetime_tweet_rate'] = acct['statuses_count'] / float(age_d)
        a_vec['A_corpus_tweet_rate'] = user['post_count'] / corpus_duration_d
        a_vec['A_interarrival_time-mean'] = iat_mean(a_iatss)
        a_vec['A_interarrival_time-stddev'] = iat_stdev(a_iatss)

        a_vecs[u_id] = a_vec

    g_iatss = interarrival_times(all_tss)
    all_ages = [a_vec['A_age'] for a_vec in a_vecs.values()]
    # graph features
    g_vec = {}
    g_vec['G_interarrival_time-mean'] = iat_mean(g_iatss)
    g_vec['G_interarrival_time-stddev'] = iat_stdev(g_iatss)
    g_vec['G_account_age-mean'] = statistics.mean(all_ages)
    g_vec['G_account_age-stddev'] = statistics.stdev(all_ages)
    g_vec['G_similarity'] = 0
    g_vec['G_density'] = (2.0 * len(E)) / (len(V) * (len(V) - 1))
    g_vec['G_shortest_path-mean'] = nx.average_shortest_path_length(hcc, weight='weight')
    g_vec['G_clustering_coefficient'] = average_clustering(hcc)
    g_vec['G_account_diversity_ratio'] = hcc_info['user_count'] / float(hcc_info['tweet_count'])

    for u_id in a_vecs:
        f_vecs[u_id] = {**a_vecs[u_id], **g_vec}


def iat_mean(iatss):
    if iatss:
        return statistics.mean(iatss)
    else:
        return -1


def iat_stdev(iatss):
    if len(iatss) > 1:
        return statistics.stdev(iatss)
    else:
        return 0


def interarrival_times(tss):
    return [tss[i + 1] - tss[i] for i in range(len(tss) - 1)]


def s_to_ts(ts_str):
    return utils.extract_ts_s(ts_str)


def s_to_d(ts_s):
    return ts_s / (60 * 60 * 24)


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    hccs_file     = opts.hccs_file
    analysis_file = opts.analysis_file
    tweets_file   = opts.tweets_file
    label         = opts.label if opts.label else 'XXX'
    out_file      = opts.out_file
    rand_hccs     = opts.random
    dry_run       = opts.dry_run

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    hccs = {}  # community_id : hcc
    g = nx.read_graphml(hccs_file)

    for hcc in (g.subgraph(c).copy() for c in nx.connected_components(g)):
        first_n = list(hcc.nodes)[0]
        c_id = hcc.nodes[first_n]['community_id']#g.nodes[list(hcc_member_ids)[0]]['community_id']
        hccs[c_id] = hcc

        # import matplotlib.pyplot as plt
        # nx.draw(hcc)
        # plt.show()

    hcc_infos = {}  # community_id : hcc_info
    with utils.open_file(analysis_file) as f:
        for l in f:
            hcc = json.loads(l)
            hcc_infos[hcc['community_id']] = hcc

    accts = {}  # account ID : profile
    line_count = 0
    min_ts = max_ts = None
    with utils.open_file(tweets_file) as f:
        for l in f:
            line_count = utils.log_row_count(line_count, DEBUG)
            t = json.loads(l)
            accts[t['user']['id_str']] = t['user']  # keep most recent
            min_ts = utils.safe_min(min_ts, s_to_ts(t['created_at']))
            max_ts = utils.safe_max(max_ts, s_to_ts(t['created_at']))
    utils.eprint('')

    corpus_duration_s = max_ts - min_ts
    corpus_duration_d = corpus_duration_s / (60 * 60 * 24)

    f_vecs = {}
    for c_id in hcc_infos:
        build_f_vecs_for(hcc_infos[c_id], hccs[c_id], accts, corpus_duration_d, f_vecs)

    columns = ['Label'] + sorted(list(list(f_vecs.values())[0].keys()))
    if dry_run:
        log('%d hccs' % nx.number_connected_components(g))
        log('%d analyses' % len(hcc_infos))
    else:
        with open(out_file, 'w', encoding='utf-8', newline='') as out_f:
            writer = csv.DictWriter(out_f, fieldnames=columns)
            writer.writeheader()
            for r in f_vecs.values():
                r['Label'] = label
                writer.writerow(r)


    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
