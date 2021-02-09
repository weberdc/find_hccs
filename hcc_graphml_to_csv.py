#!/usr/bin/env python3

import networkx as nx
import sys

from argparse import ArgumentParser
from utils import eprint


class Options:
    def __init__(self):
        self._init_parser('hcc_graphml_to_csv.py -i <weighted_undirected.graphml> [--first-int <int>] > <outfile.csv>')

    def _init_parser(self, usage):
        self.parser = ArgumentParser(usage=usage, conflict_handler='resolve')
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            default=False,
            dest='verbose',
            help='Turn on verbose logging (default: False)'
        )
        self.parser.add_argument(
            '-i', '--in-file',
            required=True,
            dest='g_file',
            help='The graphml file holding a weighted undirected graph to read.'
        )
        self.parser.add_argument(
            '--first-int',
            default=1,
            type=int,
            dest='first_int',
            help='Integer to use as first component ID'
        )

    def parse(self, argv):
        return self.parser.parse_args(argv)


DEBUG=False
def log(msg):
    if DEBUG: eprint(msg)


if __name__ == '__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    g = nx.read_graphml(opts.g_file)
    components = nx.connected_components(g)
    components = sorted(components, key=len, reverse=True)

    idx = opts.first_int
    print('node_id,community_id,proportional_degree')
    for c in components:
        degrees = list(g.subgraph(c).degree())
        all_degrees = sum(list(map(lambda pair: pair[1], degrees)))

        degrees.sort(key=lambda p: p[0])
        for (n, d) in degrees:
            print('%s,%d,%.5f' % (n, idx, d / all_degrees))

        idx += 1
