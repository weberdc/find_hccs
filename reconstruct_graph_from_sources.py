#!/usr/bin/env python

from argparse import ArgumentParser

import json
import networkx as nx
import os
import sys
import utils

# Reconstruct the filtered graph using the edge and node files produced by
# 'extract_graph_edges_by_weight.py'

class Options:
    def __init__(self):
        # self.usage = '%s' % os.path.basename(__file__)
        self.parser = ArgumentParser(conflict_handler='resolve')
        # self.parser.add_argument(
        #     '--min',
        #     dest='min_weight',
        #     type=int,
        #     default=-1,
        #     help='Keep all edges with a weight greater than this (default: -1).'
        # )
        # self.parser.add_argument(
        #     '--max',
        #     dest='max_weight',
        #     type=int,
        #     default=-1,
        #     help='Keep all edges with a weight less than this (default: -1).'
        # )
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            default=False,
            dest='verbose',
            help='Turn on verbose logging (default: False)'
        )
        # self.parser.add_argument(
        #     '-w', '--weight-property',
        #     dest='weight_property',
        #     default='weight',
        #     help='Weight property to inspect (default: "weight")'
        # )
        self.parser.add_argument(
            '-ie', '--edges-file',
            dest='edges_file',
            default='',
            required=True,
            help='File to read edges from.'
        )
        self.parser.add_argument(
            '-in', '--nodes-file',
            dest='nodes_file',
            default='',
            required=True,
            help='File to read nodes from.'
        )
        self.parser.add_argument(
            '-o',
            dest='out_file',
            default='',
            required=True,
            help='Filename for output graph file.'
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

    e_file   = opts.edges_file
    n_file   = opts.nodes_file
    out_file = opts.out_file

    g = nx.Graph()

    log('Reading nodes: %s' % n_file)
    n_count = 0
    with open(n_file, 'r', encoding='utf-8') as in_f:
        for l in in_f:
            n_count += 1
            n = json.loads(l)
            g.add_node(n['u_id'], **n['data'])
    log(f'Read {n_count:,} nodes')

    log('Reading edges: %s' % e_file)
    e_count = 0
    with open(e_file, 'r', encoding='utf-8') as in_f:
        for l in in_f:
            e_count += 1
            e = json.loads(l)
            g.add_edge(e['src'], e['tgt'], **e['data'])
    log(f'Read {e_count:,} edges')

    log('Writing graph file')
    nx.write_graphml(g, out_file)

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
