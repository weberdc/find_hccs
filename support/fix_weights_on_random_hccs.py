#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import shutil
import sys

# The random groups were created with fake edge weights. This fixes that, so
# that the weights are zero where there are no inferred connections (co-retweets)
# between nodes

def get_ot_from_rt(rt):
    if 'retweeted_status' in t:
        return t['retweeted_status']
    else:
        return None


def is_rt(t):
    return get_ot_from_rt(t) != None


def count_coretweets(id1, id2, retweeted):
    count = 0
    for ot in retweeted:
        rters = retweeted[ot]
        if id1 in rters and id2 in rters:
            count += 1
    return count


if __name__=='__main__':
    if len(sys.argv) < 3:
        print('Usage %s <hccs>.graphml <tweets>.json[.gz]' % sys.argv[0])
        sys.exit(-1)

    g_file = sys.argv[1]
    t_file = sys.argv[2]

    print('Copying file to %s.bkp' % g_file)
    shutil.copyfile(g_file, '%s.bkp' % g_file)

    print('Reading tweets and building retweet map')
    retweeted = {}
    t_f = (
        gzip.open(t_file, 'rt', encoding='utf-8')
        if t_file[-1] in 'zZ'
        else open(t_file, 'r', encoding='utf-8')
    )
    for l in t_f:
        t = json.loads(l)
        if is_rt(t):
            rter_id = t['user']['id_str']
            ot_id = get_ot_from_rt(t)['id_str']
            if ot_id not in retweeted:
                retweeted[ot_id] = [rter_id]
            else:
                retweeted[ot_id].append(rter_id)
    t_f.close()

    print('Reading graph and resetting raw_weights')
    g = nx.read_graphml(g_file)
    for u, v, d in g.edges(data=True):
        id1 = g.nodes[u]['label']
        id2 = g.nodes[v]['label']
        raw_w = count_coretweets(id1, id2, retweeted)
        g[u][v]['raw_weight'] = float(raw_w)

    print('Setting weights')
    min_w = max_w = None
    for u, v in g.edges():
        u_edges_weight = g.degree(u, weight='raw_weight')  # sum weights of edges
        v_edges_weight = g.degree(v, weight='raw_weight')
        uv_edge_weight = g[u][v]['raw_weight']
        # denom will be 1 when u and v only connect to each other
        denom = u_edges_weight + v_edges_weight - uv_edge_weight
        jaccard_factor = uv_edge_weight / float(denom) if denom else 0
        w = g[u][v]['raw_weight'] * jaccard_factor
        g[u][v]['weight'] = float(w)

        min_w = min(min_w, w) if min_w != None else w
        max_w = max(max_w, w) if max_w != None else w

    print('w_min: %f' % min_w)
    print('w_max: %f' % max_w)
    w_diff = float(max_w - min_w) if max_w != min_w else 1
    print('Setting normalised_weights')
    for u, v, w in g.edges(data='weight'):
        g[u][v]['normalised_weight'] = (w - min_w) / w_diff

    print('Writing to %s' % g_file)
    nx.write_graphml(g, g_file)
