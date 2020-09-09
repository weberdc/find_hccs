#!/usr/bin/env python

from argparse import ArgumentParser

import networkx as nx
import os
import sys
import utils

# Filter a graph's edges by edge weight

class Options:
    def __init__(self):
        self.usage = '%s [options] <term> [<term>]*' % os.path.basename(__file__)
        self.parser = ArgumentParser(usage=self.usage, conflict_handler='resolve')
        self.parser.add_argument(
            '--min',
            dest='min_weight',
            type=int,
            default=-1,
            help='Keep all edges with a weight greater than this (default: -1).'
        )
        self.parser.add_argument(
            '--max',
            dest='max_weight',
            type=int,
            default=-1,
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
            help='File to write new graph to.'
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

    in_file  = opts.in_file
    out_file = opts.out_file
    min_w    = opts.min_weight
    max_w    = opts.max_weight
    w_prop   = opts.weight_property

    log('Reading %s' % in_file)
    g = nx.read_graphml(in_file)

    log('Finding edges to remove')
    to_remove = [
        (u, v) for u, v, w in g.edges(data=w_prop)
        if min_w != -1 and w < min_w or max_w != -1 and w > max_w
    ]

    log('Removing edges')
    for u, v in to_remove:
        g.remove_edge(u, v)

    log('Finding isolates')
    to_remove = [n for n in g.nodes() if g.degree(n) == 0]
    log('Removing isolates')
    for n in to_remove:
        g.remove_node(n)

    log('Writing to %s' % out_file)
    nx.write_graphml(g, out_file)

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
