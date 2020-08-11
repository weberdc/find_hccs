#!/usr/bin/env python3

import collections
import csv
import gzip
import json
import networkx as nx
import statistics
import sys
import utils

from argparse import ArgumentParser

# Interrogates HCCs and their content and extracts various features for analysis.

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'interrogate_hccs.py --hccs <hccs>.graphml --lcn <lcn>.graphml [-b bot_analysis.json] -t <tweets_file> [--ira] -o <analysis>.json'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '--hccs',
            required=True,
            dest='hccs_file',
            help='Graphml file of HCCs'
        )
        self.parser.add_argument(
            '--lcn',
            required=True,
            dest='lcn_file',
            help='Graphml file of the original LCN'
        )
        self.parser.add_argument(
            '-t', '--tweets',
            required=True,
            dest='tweets_file',
            help='File containing HCC content'
        )
        self.parser.add_argument(
            '-b', '--botometer-results',
            default=None,
            dest='bots_file',
            help='File containing Botometer results'
        )
        self.parser.add_argument(
            '--ira',
            dest='ira',
            action='store_true',
            default=False,
            help='Tweets are in RU-IRA CSV format (default: False)'
        )
        self.parser.add_argument(
            '-o',
            required=True,
            dest='out_file',
            help='File to write the analysis to'
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


def process_json_tweet(t, tweets, retweets):
    u_id = t['user']['id_str']
    urls = utils.expanded_urls_from(t)
    ot = utils.get_ot_from_rt(t)
    is_reply = utils.is_reply(t)
    t_info = {
        't_id' : t['id_str'],
        'u_id' : u_id, #t['user']['id_str'],
        'u_sn' : t['user']['screen_name'],
        'u_dn' : t['user']['name'],
        'u_desc' : t['user']['description'],
        't_ts_sec' : utils.extract_ts_s(t['created_at']),
        'hashtags' : utils.lowered_hashtags_from(t),
        'mentioned_ids' : [m['id_str'] for m in utils.mentions_from(t)],
        'urls' : urls,
        'domains' : [utils.extract_domain(u, lower=True) for u in urls],
        'is_rt' : ot != None,
        'retweeted_t_id' : ot['id_str'] if ot else None,
        'retweeted_u_id' : ot['user']['id_str'] if ot else None,
        'is_reply' : is_reply,
        'replied_to_t_id' : t['in_reply_to_status_id_str'] if is_reply else None,
        'replied_to_u_id' : t['in_reply_to_user_id_str'] if is_reply else None,
        'text' : utils.extract_text(t)
    }
    if u_id not in tweets: tweets[u_id] = [t_info]
    else: tweets[u_id].append(t_info)
    if t_info['is_rt'] and t_info['retweeted_t_id'] not in retweets:
        retweets[t_info['retweeted_t_id']] = {
            'user_id' : t_info['retweeted_u_id'],
            'rt_text' : t_info['text']
        }


def process_ira_tweet(t, tweets, retweets):
    u_id = t['userid']
    urls = utils.parse_ira_urls(t['urls'])
    try:
        domains = [utils.extract_domain(u, lower=True) for u in urls]
    except ValueError as e:
        # assume some junk in the 'urls' field, so treat it as one URL
        domains = [utils.extract_domain(t['urls'], lower=True)]
    is_rt = t['is_retweet'] == 'true'
    is_reply = t['in_reply_to_tweetid'] != ''
    t_info = {
        't_id' : t['tweetid'],
        'u_id' : u_id,
        'u_sn' : t['user_screen_name'],
        'u_dn' : t['user_display_name'],
        'u_desc' : t['user_profile_description'],
        't_ts_sec' : utils.extract_ts_s(t['tweet_time'], fmt=utils.IRA_TS_FORMAT),
        'hashtags' : utils.parse_ira_hashtags(t['hashtags']),
        'mentioned_ids' : utils.parse_ira_mentions(t['user_mentions']),  # [m['id_str'] for m in utils.mentions_from(t)],
        'urls' : urls,
        'domains' : domains,
        'is_rt' : is_rt,
        'retweeted_t_id' : t['retweet_tweetid'] if is_rt else None,
        'retweeted_u_id' : t['retweet_userid'] if is_rt else None,
        'is_reply' : is_reply,
        'replied_to_t_id' : t['in_reply_to_tweetid'] if is_reply else None,
        'replied_to_u_id' : t['in_reply_to_userid'] if is_reply else None,
        'text' : t['tweet_text']  # utils.extract_text(t)

    }
    if u_id not in tweets: tweets[u_id] = [t_info]
    else: tweets[u_id].append(t_info)
    if t_info['is_rt'] and t_info['retweeted_t_id'] not in retweets:
        retweets[t_info['retweeted_t_id']] = {
            'user_id' : t_info['retweeted_u_id'],
            'rt_text' : t_info['text']
        }


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    STARTING_TIME = utils.now_str()
    log('Starting at %s' % STARTING_TIME)

    # read in HCCs file and determine HCCs and their members
    g = nx.read_graphml(opts.hccs_file)
    lcn_g = nx.read_graphml(opts.lcn_file)
    log('graphs loaded.')

    bot_data = {}
    if opts.bots_file:
        try:
            bot_data = utils.load_botornot_results(opts.bots_file)
        except FileNotFoundError as e:
            log('bot file missing: %s' % opts.bots_file)
    log('bot data loaded.')

    node_info = {}  # node_id : { info }
    communities = {}  # community_id : node_id
    for n, d in g.nodes(data=True):
        node_info[n] = d  # do I need to duplicate this?
        node_info[n]['_node_id'] = n
        node_info[n]['bot_results'] = bot_data[n] if n in bot_data else {}
        c_id = d['community_id']
        if c_id not in communities: communities[c_id] = [n]
        else: communities[c_id].append(n)
    log('communities constructed.')
    for u, v, d in g.edges(data=True):
        if 'normalised_weight' not in d:
            print('(%s, %s): %s' % (u, v, d))
            sys.exit()
        g[u][v]['inv_normalised_weight'] = 1.0 - d['normalised_weight']
    log('inv_normalised_weights calculated.')

    # degree
    for n, d in nx.degree(g):
        node_info[n]['degree'] = d
    for n, d in nx.degree(g, weight='normalised_weight'):
        node_info[n]['degree_w'] = d
    log('degree and weighted degree values calculated.')

    # find centralities from the original graph
    degree_centralities = nx.degree_centrality(lcn_g)
    log('degree centralities calculated.')
    # betweenness_centralities = nx.betweenness_centrality(lcn_g, weight='normalised_weight')
    # log('betweenness centralities calculated.')
    # closeness_centralities = {
    #     n : nx.closeness_centrality(lcn_g, u=n, distance='inv_normalised_weight')
    #     for n in g.nodes()
    # }
    # log('closeness centralities calculated.')
    # try:
    #     eigenvector_centralities = nx.eigenvector_centrality(lcn_g, weight='normalised_weight')
    #     log('eigenvector centralities calculated.')
    #     for n in g.nodes():
    #         node_info[n]['eigenvector_centrality'] = eigenvector_centralities[n]
    # except nx.PowerIterationFailedConvergence:
    #     utils.eprint('Eigenvector centrality failed to converge.')

    for n in g.nodes():
        node_info[n]['degree_centrality'] = degree_centralities.get(n, 0)
        # node_info[n]['betweenness_centrality'] = betweenness_centralities[n]
        # node_info[n]['closeness_centrality']   = closeness_centralities[n]

    # with open(opts.out_file, 'w', encoding='utf-8') as f:
    #     for n in node_info:
    #         f.write(json.dumps(node_info[n]))
    #         f.write('\n')

    # read in tweets, parsing them for relevant content
    tweets = {}  # user_id : [ tweet_info ]
    retweets = {}  # tweet_id : tweet_info
    t_file = opts.tweets_file
    in_f = gzip.open(t_file, 'rt', encoding='utf-8') if t_file[-1] in 'zZ' else open(t_file, 'r', encoding='utf-8')
    line_count = 0
    if opts.ira:
        csv_reader = csv.DictReader(in_f)
        for row in csv_reader:
            line_count = utils.log_row_count(line_count, DEBUG)
            process_ira_tweet(row, tweets, retweets)
    else:
        for l in in_f:
            line_count = utils.log_row_count(line_count, DEBUG)
            process_json_tweet(json.loads(l), tweets, retweets)
    log('\ntweets loaded.')

    all_tweets = {} # tweet_id : tweet_info
    for u_id in tweets:
        for t in tweets[u_id]:
            all_tweets[t['t_id']] = t
    log('full tweet map constructed.')

    # provide analysis
    community_infos = []
    for c_id in communities:
        log('community %s.... %s' % (c_id, utils.now_str()))
        community = communities[c_id]
        c_info = {
            'community_id' : c_id,
            'user_count' : len(community),
            'tweet_count' : 0,
            'rt_t_count' : 0,
            'rt_users_used' : {},
            'int_rt_t_count' : 0,  # RTs from within the community
            'int_rt_users_used' : {},  # RTed uses from within the community
            'hashtags_used' : [],
            'urls_used' : [],
            'domains_used' : [],
            'mentions_used' : [],
            'degree_centralities' : [],
            # 'closeness_centralities' : [],
            # 'betweenness_centralities' : [],
            # 'eigenvector_centralities' : [],
            'degrees' : [],
            'degree_ws' : [],
            # 'diameter' : nx.diameter(g.subgraph(community)),
            'users' : {},
            'tweets' : [],
            'tweets_by_users' : {},
            'rted_tweets' : []
        }
        log('- c_info established, now for the nodes....')
        community_infos.append(c_info)
        line_count = 0
        for n in community:
            line_count = utils.log_row_count(line_count, DEBUG)
            c_info['users'][n] = node_info[n]
            t_infos = tweets[n]  # info about n's tweets
            c_info['tweets'] += [
                {
                    't_id' : t['t_id'],
                    'u_id' : t['u_id'],
                    't_ts' : t['t_ts_sec'],
                    'text' : t['text'],
                    'is_rt': t['is_rt']
                }
                for t in tweets[n]
            ]
            c_info['tweet_count'] += len(t_infos)
            c_info['tweets_by_users'][n] = len(t_infos)
            for c_type in ['degree']: #, 'betweenness', 'closeness', 'eigenvector']:
                c_info[c_type + '_centralities'].append(node_info[n][c_type + '_centrality'])
            c_info['degrees'].append(node_info[n]['degree'])
            c_info['degree_ws'].append(node_info[n]['degree_w'])
            # log('- examining node %d tweets. %s' % (len(t_infos), utils.now_str()))
            for t_info in t_infos:
                c_info['hashtags_used'] += t_info['hashtags']
                c_info['urls_used'] += t_info['urls']
                c_info['domains_used'] += t_info['domains']
                c_info['mentions_used'] += t_info['mentioned_ids']
                if t_info['is_rt']:
                    c_info['rt_t_count'] += 1
                    c_info['rted_tweets'].append(t_info['retweeted_t_id'])
                    if t_info['retweeted_u_id'] not in c_info['rt_users_used']:
                        c_info['rt_users_used'][t_info['retweeted_u_id']] = 0
                    c_info['rt_users_used'][t_info['retweeted_u_id']] += 1
                    if t_info['retweeted_u_id'] in community:
                        if t_info['retweeted_u_id'] not in c_info['int_rt_users_used']:
                            c_info['int_rt_users_used'][t_info['retweeted_u_id']] = 0
                        c_info['int_rt_users_used'][t_info['retweeted_u_id']] += 1
                        c_info['int_rt_t_count'] += 1

        for c_type in ['degree']:  #, 'closeness', 'betweenness', 'eigenvector']:
            centralities = c_info[c_type + '_centralities']
            c_info['max_%s_centrality'  % c_type] = max(centralities)
            c_info['min_%s_centrality'  % c_type] = min(centralities)
            c_info['mean_%s_centrality' % c_type] = sum(centralities) / c_info['user_count']
            c_info['median_%s_centrality' % c_type] = statistics.median(centralities)
            del c_info[c_type + '_centralities']
        # log('- sorted centrality stats.')
        for d_type in ['degree', 'degree_w']:
            degs = c_info[d_type + 's']
            c_info['max_%s'  % d_type] = max(degs)
            c_info['min_%s'  % d_type] = min(degs)
            c_info['mean_%s' % d_type] = sum(degs) / c_info['user_count']
            c_info['median_%s' % d_type] = statistics.median(degs)
            del c_info[d_type + 's']
        # log('- sorted degree stats.')
        # turn domains_used and hashtags_used into wordcount maps, and rt_users_used and int_rt_users_used
        for x_type in ['domains', 'hashtags', 'urls', 'mentions']:
            xs = c_info[x_type + '_used']
            c_info[x_type + '_used'] = collections.Counter(xs)
        # log('- sorted entity use stats.')
        # get rt_users_used_count and int_rt_users_used_count
        c_info['rt_users_used_count'] = len(c_info['rt_users_used'])
        c_info['int_rt_users_used_count'] = len(c_info['int_rt_users_used'])
        # extract most retweeted tweets
        rt_counter = collections.Counter(c_info['rted_tweets'])
        c_info['top_rts'] = {
            t_id : {
                'count' : c,
                'acct'  : retweets[t_id]['user_id'],
                'text'  : retweets[t_id]['rt_text']
            }
            for t_id, c in rt_counter.most_common (10)
        }
        del c_info['rted_tweets']
        # log('- sorted top retweets.')
        # flesh out user details
        users_to_check = [n for n in community]
        for t in c_info['tweets']:
            u_id = t['u_id']
            if u_id in users_to_check:
                full_t = all_tweets[t['t_id']]
                c_info['users'][u_id]['screen_name'] = full_t['u_sn']
                c_info['users'][u_id]['name'] = full_t['u_dn']
                c_info['users'][u_id]['desc'] = full_t['u_desc']
        # log('- enriched users.')


    with open(opts.out_file, 'w', encoding='utf-8') as f:
        for c_info in community_infos:
            f.write(json.dumps(c_info))
            f.write('\n')

    # sub all non-qualifying characters:
    # clean_text = re.sub(r'[^A-Za-z0-9. @#]', '', full_text)


    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at    %s' % utils.now_str())
