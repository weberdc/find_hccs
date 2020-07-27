#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import random
import sys
import utils

from argparse import ArgumentParser

# basic stats for a graphml file or all graphml files in a directory

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'create_random_groups.py -i <guiding_hcc.graphml> --ids-file <ids.txt>'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default=None,
            dest='graphml_file',
            help='One graphml file'
        )
        self.parser.add_argument(
            '--tweets-file',
            default=None,
            dest='tweets_file',
            help='Tweet corpus (JSON, one tweet per line)'
        )
        self.parser.add_argument(
            '-o',
            dest='out_file',
            default=None,
            help='The output graph file (pretending to be an analysis file)'
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
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    g_file = opts.graphml_file

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    log('reading graph %s' % g_file)
    in_g = nx.read_graphml(g_file)

    t_file = opts.tweets_file
    log('reading tweets %s' % t_file)
    in_f = gzip.open(t_file, 'rt', encoding='utf-8') if t_file[-1] in 'zZ' else open(t_file, 'r', encoding='utf-8')
    post_counts = {}
    line_count = 0
    for l in in_f:
        line_count = utils.log_row_count(line_count, DEBUG)
        t = json.loads(l)
        uid = t['user']['id_str']
        if uid not in post_counts:
            post_counts[uid] = 0
        post_counts[uid] += 1
    utils.eprint()

    ids = set(post_counts.keys())
    log('Found %d accounts' % len(ids))

    taken_ids = [id for n, id in in_g.nodes(data='label')]
    for id in taken_ids:
        ids.remove(id)
    ids = list(ids)
    log('Down to %d accounts' % len(ids))

    out_g = nx.Graph()

    log('Building random groups')
    line_count = 0
    for sub_g in nx.connected_component_subgraphs(in_g):
        line_count = utils.log_row_count(line_count, DEBUG)
        c_id = [id for n, id in sub_g.nodes(data='community_id')][0]
        size = sub_g.number_of_nodes()
        fake_ids = random.choices(ids, k=size)
        for id in fake_ids:
            ids.remove(id)

        # build a clique for them
        for i in range(size-1):
            for j in range(i+1, size):
                id1 = fake_ids[i]
                id2 = fake_ids[j]

                if id1 not in out_g:
                    out_g.add_node(id1, label=id1, community_id=c_id, post_count=post_counts[id1])
                if id2 not in out_g:
                    out_g.add_node(id2, label=id2, community_id=c_id, post_count=post_counts[id2])
                out_g.add_edge(id1, id2, normalised_weight=1.0, weight=1.0, raw_weight=1.0, reason_type='RANDOM')

    utils.eprint()
    log('Writing to %s' % opts.out_file)
    nx.write_graphml(out_g, opts.out_file)

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
