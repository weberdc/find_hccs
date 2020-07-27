#!/usr/bin/env python3

import math
import networkx as nx
import net_log_utils
import os, os.path
import sys
import utils

from argparse import ArgumentParser
from pathlib import Path

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'apply_fading_sliding_window.py -i <lcn_dir> -o <lcn_dir_2> --windows <int> --alpha <float>'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            required=True,
            dest='in_lcn_dir',
            help='Directory of LCN graphml files to read.'
        )
        self.parser.add_argument(
            '-o',
            required=True,
            dest='out_lcn_dir',
            help='Directory to write combined LCN graphml files to'
        )
        self.parser.add_argument(
            '-w', '--windows',
            default=5,
            type=int,
            dest='windows',
            help='Number of windows to combine (default: 5)'
        )
        self.parser.add_argument(
            '-a', '--alpha',
            required=True,
            type=float,
            dest='alpha',
            help='Fade factor (0, 1]'
        )
        self.parser.add_argument(
            '-p', '--property',
            default='weight',
            dest='combine_property',
            help='Property to combine'
        )
        self.parser.add_argument(
            '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help='Dry run, write no files (default: False)'
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


def nodes_connected(g, u, v):
    return u in g.neighbors(v)


def combine(ordered_g_keys, cache, alpha, property):
    g_keys = ([] + ordered_g_keys)
    g_keys.reverse()
    uber_g = nx.Graph()
    first_g = cache[g_keys[0]]
    uber_g.graph['post_count'] = float(first_g.graph['post_count'])
    if 'behaviour' in first_g.graph:
        uber_g.graph['behaviour'] = first_g.graph['behaviour']

    # raw_counts = { 'nodes': 0, 'edges': 0 }  # debug
    for i in range(len(g_keys)):
        decay_factor = math.pow(alpha, i)
        g_key = g_keys[i]
        g = cache[g_key]
        # log('Graph [%d] nodes = %7d edges = %7d' % (i, g.number_of_nodes(), g.number_of_edges()))
        for n, d in g.nodes(data=True):
            # raw_counts['nodes'] += 1  # debug
            if n not in uber_g:
                uber_g.add_node(n, **d)

        for u, v, d in g.edges(data=True):
            # raw_counts['edges'] += 1  # debug
            if not nodes_connected(uber_g, u, v):
                uber_g.add_edge(u, v, **d)
                uber_g[u][v][property] = d[property] * decay_factor
            else:
                delta = d[property] * decay_factor
                uber_g[u][v][property] += delta  # d[property] * decay_factor

    # log('-> raw    nodes = %7d edges = %7d' % (raw_counts['nodes'], raw_counts['edges']))  # should differ
    # log('-> Uber_g nodes = %7d edges = %7d' % (uber_g.number_of_nodes(), uber_g.number_of_edges()))
    return uber_g


def f_to_s(alpha):
    s = [c for c in ('%f' % alpha)]
    while s[-1] == '0':
        s.pop(-1)
    if s[-1] == '.':
        s += '0'
    return ''.join(s)


def tweak_fn(fn, alpha, windows):
    first = fn[:fn.rindex('.')]
    ext = fn[fn.rindex('.')+1:]
    return '%s-a%s-w%d.%s' % (first, alpha, windows, ext)


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    STARTING_TIME = utils.now_str()
    log('Starting at %s' % STARTING_TIME)

    in_dir      = opts.in_lcn_dir
    out_dir     = opts.out_lcn_dir
    num_windows = opts.windows
    property    = opts.combine_property
    dry_run     = opts.dry_run
    alpha       = opts.alpha
    alpha_str   = f_to_s(alpha)


    if not dry_run:
        # https://stackoverflow.com/a/273227
        Path(in_dir).mkdir(parents=True, exist_ok=True)
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        log_file = net_log_utils.open_log_file(out_dir)

    g_files = list(filter(lambda f: f.endswith('graphml'), os.listdir(in_dir)))
    g_cache = {}  # to keep loaded graphs
    curr_windows = []
    line_count = 0
    for i in range(len(g_files)):
        g_file = g_files[i]

        line_count = utils.log_row_count(line_count, debug=DEBUG)

        curr_windows.append(g_file)
        if i >= num_windows:
            del g_cache[curr_windows.pop(0)]

        in_g_file = os.path.join(in_dir, g_file)
        # log('Loading %s' % in_g_file)
        g_cache[g_file] = nx.read_graphml(in_g_file)

        combined_g = combine(curr_windows, g_cache, alpha, property)

        out_g_file = os.path.join(out_dir, tweak_fn(g_file, alpha_str, num_windows))
        # log('Writing %s' % out_g_file)
        if not dry_run:
            nx.write_graphml(combined_g, out_g_file)
            # e.g., lcn-20180303_000000-15m.graphml, TODO make more efficient
            fn_ts = utils.extract_ts_s(g_file[4:19], fmt=utils.DCW_TS_FORMAT)
            net_log_utils.log_g(fn_ts, combined_g, combined_g.graph['post_count'], log_file, dry_run)

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
