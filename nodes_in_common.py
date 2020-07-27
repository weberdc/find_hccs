#!/usr/bin/env python3

import networkx as nx
import os, os.path
import statistics
import sys
import utils

from argparse import ArgumentParser

# Prints a CSV table of the nodes in common amongst the provided GraphML files,
# based on a given property

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'nodes_in_common.py <graphml file> ...'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            'g_files',
            nargs='+',
            help='GraphML files to examine'
        )
        self.parser.add_argument(
            '-p', '--id-property',
            default='id',
            dest='id_key',
            help='Name of unique node property for testing equality (default: "id")'
        )
        self.parser.add_argument(
            '-d', '--delimiter',
            default=',',
            dest='delim',
            help='String to use as delimiter (default: ",")'
        )
        self.parser.add_argument(
            '--layout',
            default=1,
            type=int,
            dest='layout',
            help='Type of table layout to use (default: 1)'
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


def count_in_common(g1, g2, id_key):
    g1_ids = set([id for id in g1.nodes(data=id_key)])
    g2_ids = set([id for id in g2.nodes(data=id_key)])
    return len(g1_ids.intersection(g2_ids))


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    g_files = opts.g_files
    id_key  = opts.id_key
    delim   = opts.delim

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    gs = { g_f : nx.read_graphml(g_f) for g_f in g_files }
    g_node_counts = { g_f : gs[g_f].number_of_nodes() for g_f in gs }
    g_edge_counts = { g_f : gs[g_f].number_of_edges() for g_f in gs }
    g_community_counts = { g_f : nx.number_connected_components(gs[g_f]) for g_f in gs }
    g_community_sizes = { g_f : list(map(len, nx.connected_component_subgraphs(gs[g_f]))) for g_f in gs }
    g_ids = {}
    for i in range(len(g_files)):
        g_ids[g_files[i]] = 'G%d' % (i + 1)

    in_common = [['-'] * len(g_files) for i in g_files]
    for r in range(len(g_files)):
        for c in range(r, len(g_files)):
            in_common[r][c] = '%d' % count_in_common(gs[g_files[r]], gs[g_files[c]], id_key)

    # header
    if opts.layout == 2:
        print(delim.join(['','Nodes','Edges','Components'] + [g_ids[g_f] for g_f in g_files]))

        for i in range(len(g_files)):
            g_f = g_files[i]
            print(delim.join([g_ids[g_f], '%d' % g_node_counts[g_f], '%d' % g_edge_counts[g_f], '%d' % g_community_counts[g_f]] + in_common[i]))

    elif opts.layout == 3:
        print(delim.join(['','Nodes','Edges','Components', 'Min.', 'Med.', 'Max.'] + [g_ids[g_f] for g_f in g_files]))

        for i in range(len(g_files)):
            g_f = g_files[i]
            print(delim.join([
                g_ids[g_f],
                '%d' % g_node_counts[g_f],
                '%d' % g_edge_counts[g_f],
                '%d' % g_community_counts[g_f],
                '%d' % min(g_community_sizes[g_f]),
                '%d' % statistics.median(g_community_sizes[g_f]),
                '%d' % max(g_community_sizes[g_f])
            ] + in_common[i]))

    else:
        print(delim.join(['','Nodes'] + [g_ids[g_f] for g_f in g_files]))
        print(delim.join(['Components', ''] + ['%d' % g_community_counts[g_f] for g_f in g_files]))

        for i in range(len(g_files)):
            g_f = g_files[i]
            print(delim.join([g_ids[g_f], '%d' % g_node_counts[g_f]] + in_common[i]))

    print()
    for g_f in g_ids:
        print('%s,%s' % (g_ids[g_f], utils.extract_filename(g_f)))

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
