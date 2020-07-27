#!/usr/bin/env python3

import json
import networkx as nx
import os
import random
import sys
import utils

from argparse import ArgumentParser

# Takes the LCN graphml files in a directory and combines them into a single
# LCN, adding up the post_counts, weights and raw_weights

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'combine_lcns.py -i <lcn_dir> -o <combined_lcn>.graphml'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i', '--lcn-dir',
            required=True,
            dest='lcn_dir',
            help='Directory of graphml files to combine (undirected, weighted)'
        )
        self.parser.add_argument(
            '-o',
            required=True,
            dest='out_file',
            help='File to write the combined LCN to'
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
    if DEBUG: utils.eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    STARTING_TIME = utils.now_str()
    log('Starting at %s' % STARTING_TIME)

    in_dir = opts.lcn_dir
    out_f = opts.out_file

    g_files = list(filter(lambda f: f.endswith('graphml'), os.listdir(in_dir)))

    uber_g = nx.Graph(post_count=0.0)

    line_count = 0
    known_reason_types = set()
    for g_file in g_files:
        g = nx.read_graphml(os.path.join(in_dir, g_file))

        ine_count = utils.log_row_count(line_count, debug=DEBUG, lines_per_dot=10, lines_per_nl=50)

        try:
            uber_g.graph['post_count'] += float(g.graph['post_count'])
        except KeyError as e:
            print(g_file)  # which file caused the issue?
            raise e

        for n, d in g.nodes(data=True):
            if n not in uber_g:
                new_d = dict([(k, d[k]) for k in d])
                new_d['post_count'] = float(new_d['post_count'])
                uber_g.add_node(n, **new_d)
            else:
                uber_g.nodes[n]['post_count'] += (d['post_count'] * 1.0)
        for u, v, d in g.edges(data=True):
            if not uber_g.has_edge(u, v):
                new_d = dict([(k, d[k]) for k in d])
                new_d['weight'] = new_d['weight'] * 1.0
                new_d['raw_weight'] = new_d['raw_weight'] * 1.0
                new_d['reasons'] = json.loads(new_d['reasons']) # unmarshal
                new_d['reason_types'] = json.loads(new_d['reason_types']) # unmarshal
                for t in new_d['reason_types']:
                    known_reason_types.add(t) # make a note of any new types
                uber_g.add_edge(u, v, **new_d)
            else:
                for k in d:
                    if k in ['weight', 'raw_weight']:
                        uber_g[u][v][k] += d[k]
                    elif k == 'reasons':
                        reasons = uber_g[u][v][k]
                        uber_g[u][v][k] = reasons + json.loads(d[k])
                    elif k == 'reason_types':
                        reason_types = json.loads(d[k])
                        for t in reason_types:
                            known_reason_types.add(t) # make a note of any new types
                            if t in uber_g[u][v][k]:  # known reason
                                uber_g[u][v][k][t] += reason_types[t] * 1.0
                            else:  # new reason
                                uber_g[u][v][k][t] = reason_types[t] * 1.0
                    else:
                        uber_g[u][v][k] = d[k]

    # prep to normalise weight property
    random_e = random.choice(list(uber_g.edges()))
    min_w = uber_g[random_e[0]][random_e[1]]['weight']  # sys.maxsize
    max_w = min_w  # sys.minsize
    for u, v, w in uber_g.edges(data='weight'):
        min_w = min(min_w, w)
        max_w = max(max_w, w)
    w_diff = float(max_w - min_w)

    known_edge_attrs = set(['normalised_weight'])
    for u, v, d in uber_g.edges(data=True):
        for k in d: known_edge_attrs.add(k)
        uber_g[u][v]['reasons'] = json.dumps(d['reasons'])
        for t in uber_g[u][v]['reason_types']:
            uber_g[u][v][t] = uber_g[u][v]['reason_types'][t] * 1.0
            known_edge_attrs.add(t)
        r_types = list(uber_g[u][v]['reason_types'].keys())
        r_types.sort()
        uber_g[u][v]['reason_types'] = '|'.join(r_types)
        uber_g[u][v]['normalised_weight'] = (d['weight'] - min_w) / w_diff

    log('known edge attrs: %s' % known_edge_attrs)
    for u, v, d in uber_g.edges(data=True):
        for attr in known_edge_attrs:
            if attr not in d:
                uber_g[u][v][attr] = 0.0

    known_node_attrs = set()
    for u, d in uber_g.nodes(data=True):
        for k in d: known_node_attrs.add(k)
    log('known node attrs: %s' % known_node_attrs)
    for u, d in uber_g.nodes(data=True):
        for attr in known_node_attrs:
            if attr not in d:
                uber_g[u][attr] = 0.0

    log('\nWriting combined graph to %s' % out_f)
    nx.write_graphml(uber_g, out_f)

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
