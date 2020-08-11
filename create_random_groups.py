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


def count_coretweets(id1, id2, retweeted):
    count = 0
    for ot in retweeted:
        rters = retweeted[ot]
        if id1 in rters and id2 in rters:
            count += 1
    return count


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
    in_f = (
        gzip.open(t_file, 'rt', encoding='utf-8')
        if t_file[-1] in 'zZ'
        else open(t_file, 'r', encoding='utf-8')
    )
    post_counts = {}
    retweeted = {}  # ot_id : [rting_acct_ids]
    line_count = 0
    for l in in_f:
        line_count = utils.log_row_count(line_count, DEBUG)
        t = json.loads(l)
        uid = t['user']['id_str']
        if uid not in post_counts:
            post_counts[uid] = 0
        post_counts[uid] += 1
        if utils.is_rt(t):
            ot_id = utils.get_ot_from_rt(t)['id_str']
            if ot_id not in retweeted:
                retweeted[ot_id] = [uid]
            else:
                retweeted[ot_id].append(uid)
    if DEBUG: utils.eprint()
    in_f.close()

    ids = set(map(str, post_counts.keys()))
    log('Found %d accounts' % len(ids))

    # forcing things to be strings, otherwise occasionally I can't remove them
    taken_ids = [str(id) for n, id in in_g.nodes(data='label')]
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
            try:
                # Sometimes this fails. I have forced all id values to be strings
                # in the hope that fixes the issue. Failing that, fail early.
                ids.remove(id)
            except e:
                # quit out early to explore further
                print('%s is missing from the list of ids' % id)
                print(json.dumps(ids))
                sys.exit(1)

        # build a clique for them
        for i in range(size-1):
            for j in range(i+1, size):
                id1 = fake_ids[i]
                id2 = fake_ids[j]

                if id1 not in out_g:
                    out_g.add_node(id1, label=id1, community_id=c_id, post_count=post_counts[id1])
                if id2 not in out_g:
                    out_g.add_node(id2, label=id2, community_id=c_id, post_count=post_counts[id2])
                raw_w = float(count_coretweets(id1, id2, retweeted))
                out_g.add_edge(id1, id2, normalised_weight=0.0, weight=0.0, raw_weight=raw_w, reason_type='RANDOM')
    if DEBUG: utils.eprint()

    min_w = max_w = None
    for u, v, d in out_g.edges(data=True):
        u_edges_weight = out_g.degree(u, weight='raw_weight')  # sum weights of edges
        v_edges_weight = out_g.degree(v, weight='raw_weight')
        uv_edge_weight = out_g[u][v]['raw_weight']
        # denom will be 1 when u and v only connect to each other
        denom = u_edges_weight + v_edges_weight - uv_edge_weight
        jaccard_factor = uv_edge_weight / float(denom) if denom else 0
        w = out_g[u][v]['raw_weight'] * jaccard_factor
        out_g[u][v]['weight'] = w

        min_w = utils.safe_min(min_w, w)
        max_w = utils.safe_max(max_w, w)

    print('w_min: %f' % min_w)
    print('w_max: %f' % max_w)
    w_diff = float(max_w - min_w) if max_w != min_w else 1
    for u, v, d in out_g.edges(data=True):
        out_g[u][v]['normalised_weight'] = (d['weight'] - min_w) / w_diff

    utils.eprint()
    log('Writing to %s' % opts.out_file)
    nx.write_graphml(out_g, opts.out_file)

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
