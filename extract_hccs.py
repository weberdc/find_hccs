#!/usr/bin/env python3

import community
import math
import networkx as nx
import random
import shutil
import statistics
import sys
import utils

from argparse import ArgumentParser

# Extracts highly coordinating communities (HCCs) from an LCN (a weighted
# undirected network) using one of a variety of strategies and writes the
# results to another graphml file.

STRATEGIES=['KNN', 'FSA_V', 'COMPONENTS', 'THRESHOLD']
class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'extract_hccs.py -i <lcn>.graphml -o <hccs>.graphml --strategy {KNN|FSA_V|COMP|THRESHOLD}'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            required=True,
            dest='lcn_file',
            help='LCN graphml file (undirected, weighted network)'
        )
        self.parser.add_argument(
            '-o',
            dest='hccs_file',
            help='File to write the HCCs graph to'
        )
        self.parser.add_argument(
            '-s', '--strategy',
            choices=STRATEGIES,
            required=True,
            dest='strategy',
            help='The extraction strategy to use'
        )
        self.parser.add_argument(
            '-t', '--threshold',
            default=0.9,
            type=float,
            dest='threshold',
            help='The normalised threshold value to use (i.e. in [0,1])'
        )
        self.parser.add_argument(
            '--theta',
            default=0.5,
            type=float,
            dest='theta',
            help='The proportional threshold value used by FSA_V'
        )
        self.parser.add_argument(
            '--weight-property',
            default='weight',
            dest='weight_property',
            help='The weight property to use (default: "weight")'
        )
        self.parser.add_argument(
            '--interactive',
            dest='interactive',
            action='store_true',
            default=False,
            help='Interactive mode for threshold decision (default: False)'
        )
        self.parser.add_argument(
            '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help='Write no files, only stats of hcc graphs (default: False)'
        )
        self.parser.add_argument(
            '--no-header',
            dest='no_header',
            action='store_true',
            default=False,
            help='When on a dry run, do not write out a CSV header (default: False)'
        )
        self.parser.add_argument(
            '-v', '--verbose',
            dest='verbose',
            action='count',
            # default=False,
            help='Verbose logging (default: False)'
        )

    def parse(self, args=None):
        return self.parser.parse_args(args)


def normalise_edge_weights(g, t_property='weight'):
    edge_weights = [w for u, v, w in g.edges(data=t_property)]
    min_w = min(edge_weights)
    max_w = max(edge_weights)

    for u, v, w in g.edges(data=t_property):
        w_norm = (w - min_w) / (max_w - min_w)  # normalise property
        g[u][v]['normalised_' + t_property] = w_norm


def ask_for_threshold(weights):
    weights.sort()
    n = len(weights)
    # quartiles = statistics.quantiles(weights, n=4)  # python 3.8 required
    quartiles = [weights[int(n / 4)], statistics.median(weights), weights[int(n * (3 / 4.0))]]
    print('Approximate statistics of graph property values:')
    print('Number of edges: %d' % n)
    print('Min:    %f' % min(weights))
    print('Q1:     %f' % quartiles[0])
    print('Median: %f' % quartiles[1])
    print('Q3:     %f' % quartiles[2])
    print('Max:    %f' % max(weights))
    print('Mean:   %f' % statistics.mean(weights))

    threshold = float(input('What threshold would you like to use? '))

    def estimate_excluded(t, sorted_list):
        for i in range(len(sorted_list)):
            if sorted_list[i] > threshold:
                break
        return i

    happy = False
    while not happy:
        excluded = estimate_excluded(threshold, weights)
        msg = 'The threshold %f will exclude %d%% of edges. Is that okay? [y/N] '
        answer = input(msg % (threshold, int((100.0 * excluded / n))))
        if not answer or answer[0] in 'Nn':
            threshold = float(input('What threshold would you like to use? '))
        else:
            happy = True

    return threshold


def apply_threshold(lcn, hccs, opts):
    threshold = opts.threshold
    t_property = opts.weight_property
    interactive = opts.interactive

    # edge_weights = [w for u, v, w in lcn.edges(data=t_property)]
    # min_w = min(edge_weights)
    # max_w = max(edge_weights)
    # normalised_edge_weights = [(w - min_w) / (max_w - min_w) for w in edge_weights]

    if interactive:
        normalised_edge_weights = [w for u, v, w in lcn.edges(data='normalised_' + t_property)]
        threshold = ask_for_threshold(normalised_edge_weights)

    if threshold < 0 or threshold > 1:
        print('Threshold %s is outside range (0,1]' % threshold)
        if threshold < 0: threshold = 0
        if threshold > 1: threshold = 1

    log('Using threshold %f' % threshold)

    for u, v, d in lcn.edges(data=True):
        w = d['normalised_' + t_property]
        # w = (d[t_property] - min_w) / (max_w - min_w)  # normalise property
        if w < threshold or u == v:  # skip self-loops
            continue
        if u not in hccs: hccs.add_node(u, **lcn.nodes[u])
        if v not in hccs: hccs.add_node(v, **lcn.nodes[v])
        new_d = { k: d[k] for k in d }
        # new_d['normalised_' + t_property] = w
        hccs.add_edge(u, v, **new_d)


def find_closest_knn(k, knns, goingup=False):
    if k in knns:
        return k
    elif k > max(knns.keys()) or k < min(knns.keys()):
        return None
    elif k == max(knns.keys()) or k == min(knns.keys()):
        return k
    else:
        delta = 1 if goingup else -1
        k = find_closest_knn(k + delta, knns, goingup)
        if k: return k
        k = find_closest_knn(k + delta, knns, not goingup)
        return k


def apply_knn(lcn, hccs, opts):
    num_accounts = lcn.number_of_nodes()
    w_property = opts.weight_property
    k = int(round(math.log(num_accounts)))
    log('Choosing k of %d (%d users)' % (k, num_accounts))
    knns = nx.k_nearest_neighbors(lcn, weight=w_property)
    closest_k = k if k in knns else find_closest_knn(k, knns)
    log('using closest_k: %d' % closest_k)
    knn = knns[closest_k] #if k in knns else knns[find_closest_knn(k, knns)]
    log('KNN: %s' % knn)

    knn_nodes = [n for n, d in lcn.degree() if d > knn]

    def prep_node_attrs(n):
        return dict([(k, lcn.nodes[k]) for k in lcn.nodes[k]])

    for u in knn_nodes:
        for v in lcn[u]:  # u's neighbours
            if v in knn_nodes:  # v qualifies
                if u not in hccs: hccs.add_node(u, **lcn.nodes[u])
                if v not in hccs: hccs.add_node(v, **lcn.nodes[v])
                if not hccs.has_edge(u, v):
                    hccs.add_edge(u, v, **lcn.edges[u, v])

    return hccs


def mean_edge_weight(g, w_key):
    weights = [w for u, v, w in g.edges(data=w_key)]
    return statistics.mean(weights) if len(weights) > 0 else 0


def apply_fsa_v(lcn, hccs, opts):
    w_property = opts.weight_property
    lcn_mean_edge_weight = mean_edge_weight(lcn, w_property)
    theta = opts.theta

    log('Mean edge weight: %.5f' % lcn_mean_edge_weight)
    if len(lcn) and 'community_id' not in list(lcn.nodes(data=True))[0][1]:
        communities = community.best_partition(lcn, weight='weight')
    else:
        # Louvain clusters have already been calculated
        communities = dict([(u, id) for u, id in lcn.nodes(data='community_id')])

    community_ids = set(communities.values())
    all_nodes = communities.keys()

    fs_list = []
    for community_id in community_ids:
        log('Examining community %d' % community_id)
        c_nodes = list(filter(lambda n: communities[n] == community_id, all_nodes))
        c_edges = [
            (u,v,w) for u,v,w in lcn.edges(nbunch=c_nodes, data=w_property)
            if u in c_nodes and v in c_nodes
        ]
        log(' - nodes %d, edges %d' % (len(c_nodes), len(c_edges)))
        fs_candidate = nx.Graph(community_id=community_id)
        if len(c_edges) == 1:
            if c_edges[0][2] >= lcn_mean_edge_weight:
                (u,v,w) = c_edges[0]
                fs_candidate.add_node(u, **lcn.nodes[u])
                fs_candidate.add_node(v, **lcn.nodes[v])
                fs_candidate.add_edge(u, v, weight=w)
            continue

        c_edges.sort(key=lambda e: e[2], reverse=True)  # sort edges by w_property, descending

        first_edge = c_edges[0]
        edge_w_data = { w_property : first_edge[2] } # use the right key
        fs_candidate.add_edge(first_edge[0], first_edge[1], **edge_w_data)

        still_growing = True
        edge_weights = [first_edge[2]]
        new_nodes = first_edge[:2]
        while still_growing:
            fs_candidate_mean_edge_weight = mean_edge_weight(fs_candidate, w_property)
            if fs_candidate_mean_edge_weight < lcn_mean_edge_weight:
                break  # our fs candidate won't get heavy enough, no fs here

            heaviest_edge = None
            ns_edges = lcn.edges(new_nodes, data=w_property)
            for u, v, w in ns_edges:
                if not fs_candidate.has_edge(u, v) and u in c_nodes and v in c_nodes:  # look within the cluster
                    if not heaviest_edge or heaviest_edge[2] < w:
                        heaviest_edge = (u, v, w)

            if not heaviest_edge:
                still_growing = False
            else:
                e_candidate = heaviest_edge
                old_mean = statistics.mean(edge_weights)
                new_mean = statistics.mean(edge_weights + [e_candidate[2]])
                median_edge_weight = statistics.median(edge_weights)
                old_stdev = statistics.stdev(edge_weights) if len(edge_weights) > 1 else old_mean # only occurs once

                if e_candidate[2] < lcn_mean_edge_weight or new_mean < old_mean - theta * old_stdev:
                    still_growing = False  # quit here
                else:
                    (u, v, w) = e_candidate
                    fs_candidate.add_node(u, **lcn.nodes[u])
                    fs_candidate.add_node(v, **lcn.nodes[v])
                    fs_candidate.add_edge(u, v, weight=w)
                    edge_weights.append(w)

                    new_nodes = [u,v]

        fs_list.append(fs_candidate)

    log('Combining focal structures')
    def prep_node_attrs(n, community_id):
        m = dict([(k, lcn.nodes[n][k]) for k in lcn.nodes[n]])
        m['community_id'] = community_id
        return m
    fs_found = 0
    # largest_fs_found = 0
    for fs in fs_list: #filter(lambda fs: len(fs) > 2, fs_list):
        fs_mean_edge_weight = mean_edge_weight(fs, 'weight')
        if fs_mean_edge_weight < lcn_mean_edge_weight:
            continue
        fs_found += 1
        c_id = fs.graph['community_id']
        log('community: %d, nodes: %d, mean edge weight %.5f' % (c_id, fs.number_of_nodes(), fs_mean_edge_weight))
        for u, v, w in fs.edges(data='weight'):
            hccs.add_node(u, **prep_node_attrs(u, c_id))
            hccs.add_node(v, **prep_node_attrs(v, c_id))
            uv_attrs = lcn.edges[u, v]  # { w_property : w }
            hccs.add_edge(u, v, **uv_attrs)

    return hccs


def apply_fsa(lcn, hccs, opts):
    pass


def add_community_labels(g):
    if g.number_of_nodes() == 0:
        return

    random_n = random.choice(list(g.nodes()))
    if 'community_id' in g.nodes[random_n]: return  # assume all nodes have this
    community_id = 0
    components = sorted(nx.connected_components(g), key=len, reverse=True)
    for c in components:
        for n in c:
            g.nodes[n]['community_id'] = community_id
        community_id += 1


def dry_run_print_graph_info(lcn, hccs, w_property, no_header):
    # print('\nLCN & HCCs:')
    # print(nx.info(hccs))
    lcn_comps = sorted(list(nx.connected_component_subgraphs(lcn)), key=len, reverse=True)
    hcc_comps = sorted(list(nx.connected_component_subgraphs(hccs)), key=len, reverse=True)

    if not no_header:
        print(
            'LCN nodes,LCN edges,LCN mean degree,LCN mean edge weight,LCN components,LCN largest component,' +
            'HCC nodes,HCC edges,HCC mean degree,HCC mean edge weight,HCC count,Largest HCC'
        )
    hccs_mean_degree = 0
    biggest_hcc_size = 0
    if hccs.number_of_nodes() > 0:
        hccs_mean_degree = statistics.mean([d for n, d in hccs.degree()])
        biggest_hcc_size = hcc_comps[0].number_of_nodes()

    print(','.join([
        '%d' % lcn.number_of_nodes(),
        '%d' % lcn.number_of_edges(),
        '%f' % statistics.mean([d for n, d in lcn.degree()]),
        '%f' % mean_edge_weight(lcn, w_property),
        '%d' % len(lcn_comps),
        '%d' % lcn_comps[0].number_of_nodes(),
        '%d' % hccs.number_of_nodes(),
        '%d' % hccs.number_of_edges(),
        '%f' % hccs_mean_degree,
        '%f' % mean_edge_weight(hccs, w_property),
        '%d' % len(hcc_comps),
        '%d' % biggest_hcc_size
    ]))



DEBUG=False
def log(msg):
    if DEBUG: utils.eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose and opts.verbose > 0

    STARTING_TIME = utils.now_str()
    log('Starting at %s' % STARTING_TIME)

    # if DEBUG: print('opts: %s' % opts)

    lcn_file  = opts.lcn_file
    hccs_file = opts.hccs_file
    strategy  = opts.strategy
    dry_run   = opts.dry_run

    if strategy == 'COMPONENTS':
        if not dry_run:
            shutil.copyfile(lcn_file, hccs_file)

    else:

        lcn = nx.read_graphml(lcn_file)
        hccs = nx.Graph()

        if dry_run:
            pass
            # print('LCN:')
            # print(nx.info(lcn))
        else:
            normalise_edge_weights(lcn, opts.weight_property)

        if lcn.number_of_nodes() == 0:
            print('Empty graph: %s' % lcn_file)
            sys.exit(1)

        if strategy == 'THRESHOLD':
            apply_threshold(lcn, hccs, opts)
        elif strategy == 'KNN':
            apply_knn(lcn, hccs, opts)
        elif strategy == 'FSA_V':
            apply_fsa_v(lcn, hccs, opts)

        add_community_labels(hccs)

        if dry_run:
            dry_run_print_graph_info(lcn, hccs, opts.weight_property, opts.no_header)
        else:  # elif hccs.number_of_nodes() > 0 and not dry_run:
            log('Writing to %s' % hccs_file)
            nx.write_graphml(hccs, hccs_file)

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
