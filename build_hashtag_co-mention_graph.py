#!/usr/bin/env python3

import csv
import gzip
import json
import networkx as nx
import sys


from argparse import ArgumentParser
from utils import lowered_hashtags_from
from raw_to_csv import parse_ira_hashtags


# Builds a graphml file of a hashtag networks, connected when hashtags are mentioned
# either by the same user, or in the same tweet (--strict)


class Options:
    def __init__(self):
        self.usage = 'build_hashtag_co-mention_graph.py -i <tweets.json> -o <outfile.graphml>'
        self._init_parser()

    def _init_parser(self):

        self.parser = ArgumentParser(usage=self.usage,conflict_handler='resolve')
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            default=False,
            dest='verbose',
            help='Turn on verbose logging (default: False)'
        )
        self.parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            dest='dry_run',
            help='Dry run mode - will not write to outfile (default: False)'
        )
        self.parser.add_argument(
            '--strict',
            action='store_true',
            default=False,
            dest='strict',
            help='Only link hashtags occurring in the same tweet (default: False)'
        )
        self.parser.add_argument(
            '--ira',
            action='store_true',
            default=False,
            dest='ira',
            help='Expect data in Twitter\'s election integrity format (CSV) (default: False)'
        )
        self.parser.add_argument(
            '-i',
            dest='in_file',
            required=True,
            help='File of tweets to read.'
        )
        self.parser.add_argument(
            '-o',
            dest='out_file',
            required=True,
            help='GraphML file to write hashtag graph to.'
        )
        self.parser.add_argument(
            '--ignore',
            dest='ignore_hashtags',
            default='',
            help='Hashtags to ignore (default: filenames)'
        )
        self.parser.add_argument(
            '--min-weight',
            dest='min_weight',
            default=1,
            type=int,
            help='Smallest permitted count of co-mentioning authors (default: 1)'
        )



    def parse(self, args=None):
        return self.parser.parse_args(args)


def add_nodes(g, *nodes):
    for n in nodes:
        if n not in g:
            g.add_node(n, label=n)


def add_weighted_edge(g, u, v, delta=1, weight_property='weight'):
    if not g.has_edge(u, v):
        g.add_edge(u, v)
        g[u][v][weight_property] = 0.0
    g[u][v][weight_property] += float(delta)


def process(user_id, hashtags, users_hashtags, cooccurring_hashtags):
    if user_id not in users_hashtags:
        users_hashtags[user_id] = dict([(ht, 1) for ht in hashtags])
    else:
        for ht in hashtags:
            if ht not in users_hashtags[user_id]:
                users_hashtags[user_id][ht] = 0
            users_hashtags[user_id][ht] += 1
    if len(hashtags) > 1:
        hashtags.sort()
        ht1_idx = 0
        ht2_idx = 1
        for ht1_idx in range(0, len(hashtags) - 1):
            for ht2_idx in range(ht1_idx + 1, len(hashtags)):
                key = (hashtags[ht1_idx], hashtags[ht2_idx])
                if key not in cooccurring_hashtags:
                    cooccurring_hashtags[key] = 0
                cooccurring_hashtags[key] += 1



def log_row(tweet_count):
    tweet_count += 1
    if DEBUG and tweet_count %  100 == 0: eprint('.', end='')
    if DEBUG and tweet_count % 5000 == 0: eprint(' %10d' % tweet_count)
    return tweet_count


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

    in_file    = opts.in_file
    out_file   = opts.out_file
    to_ignore  = opts.ignore_hashtags.split(',')
    min_weight = opts.min_weight
    dry_run    = opts.dry_run
    strict     = opts.strict
    ira        = opts.ira

    log('In JSON:     %s' % in_file)
    log('Out GraphML: %s' % out_file)
    log('Ignore:      %s' % ','.join(to_ignore))
    log('Min weight:  %d' % min_weight)
    log('Dry run:     %s' % dry_run)
    log('Strict:      %s' % strict)
    log('IRA:         %s' % ira)

    # record the hashtag uses
    users_hashtags = {}  # user_id : map(hashtags:counts)
    cooccurring_hashtags = {}  # (ht1, ht2) : count, ht1 < ht2
    tweet_count = 0

    # in_f = gzip.open(in_file, 'rt', encoding='utf-8') if in_file[-1] in 'zZ' else open(in_file, 'r', encoding='utf-8')
    if ira:
        in_f = gzip.open(in_file, 'rt', encoding='utf-8') if in_file[-1] in 'zZ' else open(in_file, 'r', encoding='utf-8')
    else:
        in_f = gzip.open(in_file, 'rt') if in_file[-1] in 'zZ' else open(in_file, 'r', encoding='utf-8')
    if not ira:
        # with open(in_file, 'r', encoding='utf-8') as f:
        for line in in_f: #f.readlines():
            tweet_count = log_row(tweet_count)

            tweet = json.loads(line)
            user_id = tweet['user']['id_str']
            hashtags = [ht for ht in lowered_hashtags_from(tweet) if ht not in to_ignore]

            process(user_id, hashtags, users_hashtags, cooccurring_hashtags)

    else: # ira
        csv_reader = csv.DictReader(in_f)
        for tweet in csv_reader:
            tweet_count = log_row(tweet_count)

            user_id = tweet['userid']
            hashtags = [ht for ht in parse_ira_hashtags(tweet['hashtags']) if ht not in to_ignore]

            process(user_id, hashtags, users_hashtags, cooccurring_hashtags)

    in_f.close()


    log('')
    log('Tweets: %d' % tweet_count)
    log('Users: %d' % len(users_hashtags))

    # make the graph
    g = nx.Graph()
    if not strict:
        for ht_counts in filter(lambda hts: len(hts) > 1, users_hashtags.values()):
            hts_to_link = list(ht_counts.keys())
            ht_1 = hts_to_link[0]
            for ht_n in hts_to_link[1:]:
                add_nodes(g, ht_1, ht_n)
                add_weighted_edge(g, ht_1, ht_n)
    else:
        for uv in cooccurring_hashtags:
            add_nodes(g, uv[0], uv[1])
            add_weighted_edge(g, uv[0], uv[1], delta=cooccurring_hashtags[uv])

    # strip light edges
    if min_weight > 1:
        unwanted = [(u, v) for u, v, d in g.edges(data=True) if d['weight'] < min_weight]
        # for u, v, d in g.edges(data=True):
        #     if d['weight'] < min_weight:
        #         unwanted.append( (u, v) )
        g.remove_edges_from(unwanted)
        unwanted = list(map(lambda pair: pair[0], filter(lambda pair: pair[1] == 0, g.degree())))
        g.remove_nodes_from(unwanted)

    # write the graph
    if not dry_run:
        nx.write_graphml(g, out_file)

    print('DONE - Hashtag Graph[nodes=%d,edges=%d,components=%d]' % (
        len(g), len(g.edges()), nx.number_connected_components(g)
    ))
