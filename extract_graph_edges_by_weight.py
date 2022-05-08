#!/usr/bin/env python

from argparse import ArgumentParser

import json
import networkx as nx
import os
import sys
import utils

# Extract a graph's edges by edge weight, when the graph is very large.
#
# Traverses a graph's edges writing out the edge information while it does
# so, to avoid keeping it in memory. Nodes adjacent to these edges are noted
# and written out subsequently, leaving two files ready to be used to
# reconstruct the filtered graph using 'build_graph_from_sources.py'

class Options:
    def __init__(self):
        self.usage = '%s' % os.path.basename(__file__)
        self.parser = ArgumentParser(usage=self.usage, conflict_handler='resolve')
        self.parser.add_argument(
            '--min',
            dest='min_weight',
            type=float,
            default=-1.0,
            help='Keep all edges with a weight greater than this (default: -1).'
        )
        self.parser.add_argument(
            '--max',
            dest='max_weight',
            type=float,
            default=-1.0,
            help='Keep all edges with a weight less than this (default: -1).'
        )
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            default=False,
            dest='verbose',
            help='Turn on verbose logging (default: False)'
        )
        self.parser.add_argument(
            '-w', '--weight-property',
            dest='weight_property',
            default='weight',
            help='Weight property to inspect (default: "weight")'
        )
        self.parser.add_argument(
            '-i',
            dest='in_file',
            default='',
            required=True,
            help='File to read graph from.'
        )
        self.parser.add_argument(
            '-o',
            dest='out_file',
            default='',
            required=True,
            help='Filename base for node and edge files.'
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
    out_fb  = opts.out_file
    min_w   = opts.min_weight
    max_w   = opts.max_weight
    w_prop  = opts.weight_property

    log('Reading %s' % in_file)
    g = nx.read_graphml(in_file)

    log(f'Read graph, V={g.number_of_nodes():,} E={g.number_of_edges():,}')

    log('Finding edges to remove')
    nodes_to_keep = set()  # ids of nodes to retrieve later
    edges_kept = 0
    with open(f'{out_fb}-edges.json', 'w', encoding='utf-8') as out_f:
        for u, v, d in g.edges(data=True):
            w = float(d[w_prop])
            if (min_w < 0 or w >= min_w) and (max_w < 0 or w <= max_w):
                edges_kept += 1
                nodes_to_keep.add(u)
                nodes_to_keep.add(v)
                out_f.write(json.dumps({
                    'src' : u,
                    'tgt' : v,
                    'data': d
                }))
                out_f.write('\n')

    log(f'Kept edges: {edges_kept:,}')
    log(f'Keeping nodes: {len(nodes_to_keep):,}')
    with open(f'{out_fb}-nodes.json', 'w', encoding='utf-8') as out_f:
        for u, d in g.nodes(data=True):
            if u in nodes_to_keep:
                out_f.write(json.dumps({
                    'u_id': u,
                    'data': d
                }))
                out_f.write('\n')

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
