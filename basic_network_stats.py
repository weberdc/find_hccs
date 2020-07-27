#!/usr/bin/env python3

import networkx as nx
import os, os.path
import sys
import utils

from argparse import ArgumentParser

# basic stats for a graphml file or all graphml files in a directory

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'basic_network_stats.py -i <graphml file>|<dir of graphml files>'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default=None,
            dest='graphml_path',
            help='One graphml file or a path to a directory of them'
        )
        self.parser.add_argument(
            '--hccs',
            dest='hccs',
            action='store_true',
            default=False,
            help='Output for HCCs specifically (default: False)'
        )
        self.parser.add_argument(
            '--skip-header',
            dest='skip_header',
            action='store_true',
            default=False,
            help='Do not print the CSV header (default: False)'
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


def method_to_str(m):
    if m.startswith('knn'):
        return 'kNN'
    elif m.startswith('fsa'):
        return 'FSA_V'
    else:
        return 'Threshold'


def parse_hcc_filename(fn):
    # sapol-retweets-1440m-0.9-hccs-fsa_v_0.5.graphml  sapol-retweets-15m-hccs-t_0.3.graphml           sapol-retweets-60m-0.7-hccs-knn.graphml
    # sapol-retweets-1440m-0.9-hccs-knn.graphml        sapol-retweets-15m-hccs-threshold_0.3.graphml   sapol-retweets-60m-0.7-hccs-t_0.3.graphml
    # sapol-retweets-1440m-0.9-hccs-t_0.3.graphml      sapol-retweets-360m-0.5-hccs-fsa_v_0.5.graphml  sapol-retweets-60m-0.9-hccs-fsa_v_0.5.graphml
    parts = fn.split('-')
    info = { 'corpus' : parts[0], 'behaviour' : parts[1], 'window' : parts[2] }
    if parts[3] == 'hccs':
        info['alpha'] = '-'
        info['method'] = method_to_str(parts[4])
    else:
        info['alpha'] = parts[3]
        info['method'] = method_to_str(parts[5])
    return info


def mean_edge_weight(g, weight):
    weights = [w for u, v, w in g.edges(data=weight)]
    return sum(weights) / float(len(weights))


def mean_degree(g, weight=None):
    degrees = nx.degree(g, weight=weight)
    return sum([d for n, d in degrees]) / float(len(degrees))


def report_on_hccs(g_dir, skip_header):
    if not skip_header:
        print('Dir:,%s' % g_dir)
        print('Filename,Corpus,Window,Alpha,Method,Nodes,Edges,Components,Mean Degree,Mean Weighted Degree,Mean Edge Weight')
    g_files = list(filter(lambda f: f.endswith('graphml'), os.listdir(g_dir)))
    for g_fn in g_files:
        g = nx.read_graphml(os.path.join(g_dir, g_fn))
        info = parse_hcc_filename(g_fn)
        print(','.join([
            g_fn, info['corpus'], info['window'], info['alpha'], info['method'],
            '%d' % g.number_of_nodes(), '%d' % g.number_of_edges(),
            '%d' % nx.number_connected_components(g),
            '%s' % mean_degree(g),
            '%s' % mean_degree(g, weight='normalised_weight'),
            '%s' % mean_edge_weight(g, 'normalised_weight')
        ]))


def report_on(g_dir, g_file):
    g = nx.read_graphml(os.path.join(g_dir, g_file))
    print('%s,%d,%d,%d' % (
        utils.extract_filename(g_file), g.number_of_nodes(), g.number_of_edges(),
        nx.number_connected_components(g)
    ))


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    g_path = opts.graphml_path
    skip_header = opts.skip_header

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    if opts.hccs:
        report_on_hccs(g_path, skip_header)
    else:
        if not skip_header:
            print('Dir:,%s' % g_path)
            print('Filename,Nodes,Edges,Components')
        if not os.path.isdir(g_path):
            report_on('.', g_path)
        else:
            g_files = list(filter(lambda f: f.endswith('graphml'), os.listdir(g_path)))
            for g_fn in g_files:
                report_on(g_path, g_fn)

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
