#!/usr/bin/env python3

import csv
import json
import networkx as nx
import sys

from argparse import ArgumentParser
from utils import eprint, open_file  #, expanded_urls_from, extract_ts, fetch_lines, get_uid, get_rt, lowered_hashtags_from

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'find_behaviour.py -i tweets_info.csv[.gz] -o <lcn.graphml> --targets "RETWEET:ot_id|MENTION:target"' # <target column name> --behaviour [RETWEET|HASHTAG|URL|DOMAIN|MENTION|IN_CONV]'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default='-',
            dest='csv_file',
            help='CSV file of tweet info (end filename with z for gzip)'
        )
        self.parser.add_argument(
            '-o',
            default='-',
            dest='lcn_file',
            help='GraphML file with resulting LCN'
        )
        # self.parser.add_argument(
        #     '-t', '--target',
        #     default='target',
        #     dest='matching_field',
        #     help='Column to use to match rows (default: "target")'
        # )
        self.parser.add_argument(
            '-t', '--targets',
            # default='target',
            required=True,
            dest='targets',
            help='Behaviours and matching columns to use to match rows, separated by pipes (e.g., "RETWEET:ot_id|MENTION:target")'
        )
        # self.parser.add_argument(
        #     '-b', '--behaviour',
        #     choices=['RETWEET', 'HASHTAG', 'URL', 'DOMAIN', 'MENTION', 'IN_CONV'],
        #     dest='behaviour',
        #     help='Determines the behaviour to detect'
        # )
        self.parser.add_argument(
            '-v', '--verbose',
            dest='verbose',
            action='store_true',
            default=False,
            help='Verbose logging (default: False)'
        )

    def parse(self, args=None):
        return self.parser.parse_args(args)


def word_count(words):
    wc = {}
    for w in set(words):
        wc[w] = words.count(w)
    return wc


class Detective:
    def __init__(self, behaviours=None):
        self.behaviours = behaviours

    def _check_node_exists(self, g, n):
        if n in g:
            g.nodes[n]['post_count'] += 1.0
        else:
            g.add_node(n, label=n, post_count=1.0)

    def _add_edge(self, g, n1, n2, reason, interaction_type):
        # print('n1: %s, type(n1): %s' % (n1, type(n1)))
        if g.has_edge(n1, n2):
            g[n1][n2]['reasons'].append(reason)
            g[n1][n2]['reason_types'].append(interaction_type)
        else:
            g.add_edge(n1, n2, reasons=[reason], reason_types=[interaction_type])

    def gather_evidence(self, tweet_rows, behaviours_and_fields): #matching_field='target'):
        # def reason_types_to_s(r_types):
        #     just_types = list(set(r_types))
        #     just_types.sort()  # alphabetically
        #     return ','.join(just_types)

        num_rows = len(tweet_rows)
        g_attrs = { 'post_count' : num_rows }
        if self.behaviours: g_attrs['behaviours'] = self.behaviours
        g = nx.Graph(**g_attrs)

        log('num_rows: %d' % num_rows)
        for i in range(num_rows - 1):
            for j in range(i + 1, num_rows):
                t1 = tweet_rows[i]
                t2 = tweet_rows[j]

                matching_field = behaviours_and_fields[t1['interaction']]
                if (t1['source'] != t2['source'] and
                    t1['interaction'] == t2['interaction'] and
                    t1[matching_field] == t2[matching_field]):
                    self._check_node_exists(g, t1['source'])
                    self._check_node_exists(g, t2['source'])
                    self._add_edge(g, t1['source'], t2['source'], t1[matching_field], t1['interaction'])
                    # self._add_edge(g, t1['source'], t2['source'], behaviours_and_fields[t1['interaction']], t1['interaction'])

        for u, v, d in g.edges(data=True):
            if 'reasons' in g[u][v]:
                g[u][v]['raw_weight'] = len(g[u][v]['reasons']) * 1.0

                u_edges_weight = g.degree(u, weight='raw_weight')  # sum weights of edges
                v_edges_weight = g.degree(v, weight='raw_weight')
                uv_edge_weight = g[u][v]['raw_weight']
                # denom will be 1 when u and v only connect to each other
                denom = u_edges_weight + v_edges_weight - uv_edge_weight
                jaccard_factor = uv_edge_weight / float(denom)
                g[u][v]['weight'] = g[u][v]['raw_weight'] * jaccard_factor

                g[u][v]['reasons'] = json.dumps(g[u][v]['reasons'])

                reason_types = g[u][v]['reason_types']
                g[u][v]['reason_types'] = json.dumps(word_count(reason_types))
                # g[u][v]['reason_types'] = reason_types_to_s(reason_types)
                # for r in set(reason_types):
                #     g[u][v][r] = reason_types.count(r) * 1.0

        log('Network built from %d tweets [nodes=%d,edges=%d]' % (num_rows, g.number_of_nodes(), g.number_of_edges()))
        return g


def parse_targets_cli(cli_arg):
    return { b : t for b, t in [p.split(':') for p in cli_arg.split('|')] }


DEBUG=False
def log(msg):
    if DEBUG: eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    csv_file = opts.csv_file
    g_file = opts.lcn_file
    # behaviour = opts.behaviour
    # matching_field = opts.matching_field

    behaviours_and_fields = parse_targets_cli(opts.targets)  #{ b : t for b, t in [p.split(':') for p in opts.targets.split('|')] }
    behaviours = '|'.join(sorted(list(behaviours_and_fields.keys())))

    log('In:  %s' % csv_file)
    log('Out: %s' % g_file)
    log('Behav.: %s' % behaviours)

    # TODO add targets to ignore

    tweet_rows = []
    with open_file(csv_file) as in_f:
        reader = csv.DictReader(in_f)

        for row in reader:
            tweet_rows.append(row)

    d = Detective(behaviours)
    g = d.gather_evidence(tweet_rows, behaviours_and_fields)

    nx.write_graphml(g, g_file)
