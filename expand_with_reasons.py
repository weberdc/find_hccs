#!/usr/bin/env python3

import json
import networkx as nx
import sys
import utils

from argparse import ArgumentParser

# Adds to an HCC based on the 'reasons' field of its edges, which indicate why
# two vertices are connected.

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'decorate_network.py -i <graphml HCC file> -o <graphml file>'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            required=True,
            dest='graphml_file',
            help='A graphml file to decorate'
        )
        self.parser.add_argument(
            '-o',
            required=True,
            dest='out_file',
            help='Where to write the expanded graph'
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


def add_reason_node(g, r):
    g.add_node(r, label=r, _node_type='REASON')


def link_to_reason(g, n, r):
    if not g.has_edge(n, r):
        g.add_edge(n, r, weight=1.0, _edge_type='REASON')
    else:
        g[n][r]['weight'] += 1.0


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    in_file = opts.graphml_file
    out_file = opts.out_file

    g = nx.read_graphml(in_file)

    for n in g.nodes():
        g.nodes[n]['_node_type'] = 'ACCOUNT'

    to_add = []
    for u, v, r_json in g.edges(data='reasons'):
        reasons = json.loads(r_json)
        for r in reasons:
            to_add.append( (u, v, r) )

    for u, v, r in to_add:
        if r not in g: add_reason_node(g, r)
            # g.add_node(r, label=r, _node_type='REASON')
        link_to_reason(g, u, r)
        link_to_reason(g, v, r)
        # if not g.has_edge(u, r):
        #     g.add_edge(u, r, weight=1.0, _edge_type='REASON')
        # else:
        #     g[u][r]['weight'] += 1.0
        # if not g.has_edge(v, r):
        #     g.add_edge(v, r, weight=1.0, _edge_type='REASON')
        # else:
        #     g[v][r]['weight'] += 1.0

    nx.write_graphml(g, out_file)

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
