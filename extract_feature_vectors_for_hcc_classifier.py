#!/usr/bin/env python3

import csv
import gzip
import json
import networkx as nx
import sys
import time
import utils

from argparse import ArgumentParser
from calculate_activity_network import embedded_extended_tweet_url, root_of_conversation
from collections import defaultdict
from datetime import datetime
from utils import eprint, expanded_urls_from, extract_text, flatten, lowered_hashtags_from, mentioned_ids_from#, timestamp_2_epoch_seconds


# Builds feature vectors for HCC members and their groupings as input to the
# classifiers for validation
#
# This version extracts 32 features


class Options():
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'extract_feature_vectors_for_hcc_classifier.py -t <tweets.json> -i <ids.csv> -l <label>'
        self.parser = ArgumentParser(usage=usage,conflict_handler='resolve')

        self.parser.add_argument(
            '-t', '--tweets',
            required=True,
            dest='tweets_file',
            help='File containing all the tweets'
        )
        self.parser.add_argument(
            '-i', '--ids-file',
            required=True,
            dest='ids_file',
            help='The list of IDs to build feature vectors for.'
        )
        self.parser.add_argument(
            '-l', '--label',
            required=True,
            dest='label',
            help='The label to apply to each entry in the data generated (first column).'
        )
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            default=False,
            dest='verbose',
            help='Turn on verbose logging (default: False)'
        )

    def parse(self, args=None):
        return self.parser.parse_args(args)


TWITTER_TS_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'  # Tue Apr 26 08:57:55 +0000 2011
def parse_ts(ts_str):
    time_struct = time.strptime(ts_str, TWITTER_TS_FORMAT)
    return datetime.fromtimestamp(time.mktime(time_struct))


def count(fltr): return len(list(fltr))


def root_of_conversation(tweet_in_conversation, tweet_map):
    """Finds the root of the conversation that the provided tweet is in"""
    root_id = tweet_in_conversation
    # go until we reply outside of the corpus, or the current tweet isn't a reply
    while root_id in tweet_map and 'in_reply_to_status_id_str' in tweet_map[root_id] and tweet_map[root_id]['in_reply_to_status_id_str']:
        root_id = tweet_map[root_id]['in_reply_to_status_id_str']
    return root_id


def embedded_extended_tweet_url(tweet_id, url):
    # extended tweets, because their text field is not long enough for the
    # content, they include an embedded url pointing to the full tweet
    # Of course, this isn't the sort of URL we're interested in, so we can
    # test for it so we can strip it out. This method identifies it.
    return url == 'https://twitter.com/i/web/status/%s' % tweet_id



USER_FEATURES = [
    'U_tweet_count',
    'U_retweet_count',
    'U_reply_count',
    'U_tweet_rate',
    'U_mentioned_ids',  # unique IDs
    'U_mention_count', # every mention
    'U_unique_hts',  # unique hashtags
    'U_ht_count', # every hashtag
    'U_unique_urls',  # unique hashtags
    'U_url_count', # every hashtag
    'U_default_img',
    'U_desc_len',
    'U_url'
]
DEFAULT_PROF_IMG_URL = 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
def build_user_feature_vector(u_id, activity, collection_period_mins):
    profile = activity[0]['user']
    return {
        'U_tweet_count'   : len(activity),
        'U_retweet_count' : count(filter(lambda t: 'retweeted_status' in t and t['retweeted_status'], activity)),
        'U_reply_count'   : count(filter(lambda t: t['in_reply_to_status_id_str'], activity)),
        'U_tweet_rate'    : len(activity) / collection_period_mins,
        'U_mentioned_ids' : len(set(flatten(map(mentioned_ids_from, activity)))),  # unique IDs
        'U_mention_count' : len(list(flatten(map(mentioned_ids_from, activity)))), # every mention
        'U_unique_hts'    : len(set(flatten(map(lowered_hashtags_from, activity)))),  # unique hashtags
        'U_ht_count'      : len(list(flatten(map(lowered_hashtags_from, activity)))), # every hashtag
        'U_unique_urls'   : len(set(flatten(map(expanded_urls_from, activity)))),  # unique hashtags
        'U_url_count'     : len(list(flatten(map(expanded_urls_from, activity)))), # every hashtag
        'U_default_img'   : 1 if profile['profile_image_url'] == DEFAULT_PROF_IMG_URL else 0,
        'U_desc_len'      : len(profile['description'] if profile['description'] else ''),
        'U_url'           : len(profile['url'] if profile['url'] else ''),
    }


COMMUNITY_FEATURES = [
    'C_tweet_count',
    'C_node_count',
    'C_edge_count',
    'C_user_count',
    'C_author_count',
    'C_hashtag_count',
    'C_url_count',
    'C_repost_count',
    'C_quote_count',
    'C_mention_count',
    'C_reply_count',
    'C_use_ht_count',
    'C_use_url_count',
    'C_in_conv_count',
    'C_in/ext_repost',
    'C_in/ext_mention',
    'C_in/ext_reply',
]
def build_community_feature_vector(community, g):
    def count_nodes_if(cond):
        return len([n for n, d in g.nodes(data=True) if cond(n, d)])
    def count_edges_if(cond):
        return len([k for u, v, k, d in g.edges(data=True,keys=True) if cond(u, v, k, d)])  # d['interaction'] == t]
        # return len(['x' for u, v, d in g.edges(data=True) if cond(u, v, d)])
    int_users = [n for n, d in g.nodes(data=True) if d['is_author']]
    ext_users = [n for n, d in g.nodes(data=True) if d['n_type'] == 'USER' and not d['is_author']]
    repost_count   = count_edges_if(lambda u, v, k, d: d['interaction'] == 'REPOST')
    reply_count    = count_edges_if(lambda u, v, k, d: d['interaction'] == 'REPLY')
    mention_count  = count_edges_if(lambda u, v, k, d: d['interaction'] == 'MENTION')
    return {
        'C_tweet_count'    : g.graph['post_count'],
        'C_node_count'     : len(g),
        'C_edge_count'     : len(g.edges()),
        'C_user_count'     : count_nodes_if(lambda n, d: d['n_type'] == 'USER'),
        'C_author_count'   : count_nodes_if(lambda n, d: d['n_type'] == 'USER' and d['is_author']),
        'C_hashtag_count'  : count_nodes_if(lambda n, d: d['n_type'] == 'HASHTAG'),
        'C_url_count'      : count_nodes_if(lambda n, d: d['n_type'] == 'URL'),
        'C_repost_count'   : repost_count,
        'C_quote_count'    : count_edges_if(lambda u, v, k, d: d['interaction'] == 'QUOTE'),
        'C_mention_count'  : mention_count,
        'C_reply_count'    : reply_count,
        'C_use_ht_count'   : count_edges_if(lambda u, v, k, d: d['interaction'] == 'HASHTAG'),
        'C_use_url_count'  : count_edges_if(lambda u, v, k, d: d['interaction'] == 'URL'),
        'C_in_conv_count'  : count_edges_if(lambda u, v, k, d: d['interaction'] == 'IN_CONVERSATION'),
        'C_in/ext_repost'  : count_edges_if(lambda u, v, k, d: d['interaction'] == 'REPOST' and v in int_users) / repost_count if repost_count else 0,
        'C_in/ext_mention' : count_edges_if(lambda u, v, k, d: d['interaction'] == 'MENTION' and v in int_users) / mention_count if mention_count else 0,
        'C_in/ext_reply'   : count_edges_if(lambda u, v, k, d: d['interaction'] == 'REPLY' and v in int_users) / reply_count if reply_count else 0
    }


def mk_feature_str(keys, feature_map):
    return ','.join([str(feature_map[k]) for k in keys])


def build_activity_graph(tweets, t_0):  # tweets is a tweet map { tweet_id : tweet }
    first_tweet_ts_str = utils.ts_to_str(t_0, fmt=utils.TWITTER_TS_FORMAT)  # epoch_seconds_2_timestamp_str(t_0)
    first_tweet_ts = utils.epoch_seconds_2_ts(t_0)  #first_tweet_ts_str)  # parse_twitter_ts(first_tweet_ts_str)
    g = nx.MultiDiGraph(post_count=len(tweets))

    def add_node(g, n_id, n_type='USER', is_author=False):
        if n_id not in g:
            g.add_node(n_id, n_type=n_type, label=n_id, is_author=is_author)
        elif is_author:
            # g.nodes[n_id]['n_type'] = n_type
            g.nodes[n_id]['is_author'] = is_author

    def node_type_for(interaction):
        if interaction == 'HASHTAG' or interaction == 'URL':
            return interaction
        else:
            return 'USER'

    def add_edge(g, from_id, to_id, tweet_id, ts_str, int_type, **kwargs):
        add_node(g, from_id, 'USER', True)
        # g.nodes[from_id]['is_author'] = True
        add_node(g, to_id, n_type=node_type_for(int_type))
        t = utils.extract_ts_s(ts_str) - t_0  # timestamp_2_epoch_seconds(utils.extract_ts_s(ts_str)) - t_0
        attrs = {
            'time_t' : t,
            'tweet_id' : tweet_id,
            'interaction' : int_type
        }
        key = '%s %s %s in %s' % (from_id, int_type, to_id, tweet_id)
        g.add_edge(from_id, to_id, key=key, **{**attrs, **kwargs})

        # Build networks
    # edge types: REPOST, MENTION, REPLY, QUOTE, URL, HASHTAG
    observed_user_ids = set()
    for tweet_id in tweets:
        tweet = tweets[tweet_id]
        hashtags = lowered_hashtags_from(tweet)
        urls = expanded_urls_from(tweet)
        mentions = mentioned_ids_from(tweet)
        tweet_text = extract_text(tweet)
        tweet_ts = tweet['created_at']
        tweet_id = tweet['id_str']
        tweeter_id = tweet['user']['id_str']
        observed_user_ids.add(tweeter_id)

        for ht in hashtags:
            add_edge(g, tweeter_id, ht, tweet_id, tweet_ts, 'HASHTAG')
        for url in urls:
            if not embedded_extended_tweet_url(tweet_id, url):  # extended tweets include a URL to their extended form
                add_edge(g, tweeter_id, url, tweet_id, tweet_ts, 'URL')
        for mentioned_id in mentions:
            observed_user_ids.add(mentioned_id)
            add_edge(g, tweeter_id, mentioned_id, tweet_id, tweet_ts, 'MENTION')

        if 'retweeted_status' in tweet:
            retweeter = tweeter_id
            retweetee = tweet['retweeted_status']['user']['id_str']
            observed_user_ids.add(retweetee)
            add_edge(
                g, retweeter, retweetee, tweet_id, tweet_ts, 'REPOST',
                original_tweet_id=tweet['retweeted_status']['id_str'],
                original_tweet_ts=tweet['retweeted_status']['created_at'],
                posting_delay_sec=(
                    utils.extract_ts_s(tweet['retweeted_status']['created_at']) -
                    utils.extract_ts_s(tweet_ts)
                )#.total_seconds()
            )
        elif 'quoted_status' in tweet and 'retweeted_status' not in tweet:
            quoter = tweeter_id
            quotee = tweet['quoted_status']['user']['id_str']
            observed_user_ids.add(quotee)
            add_edge(
                g, quoter, quotee, tweet_id, tweet_ts, 'QUOTE',
                original_tweet_id=tweet['quoted_status']['id_str'],
                original_tweet_ts=tweet['quoted_status']['created_at'],
                posting_delay_sec=(
                    utils.extract_ts_s(tweet['quoted_status']['created_at']) -
                    utils.extract_ts_s(tweet_ts)
                )#.total_seconds()
            )
        elif 'in_reply_to_status_id_str' in tweet and tweet['in_reply_to_status_id_str'] in tweets:
            # only consider replies that appear in the corpus
            # basic reply info
            replier = tweeter_id
            replied_to = tweet['in_reply_to_user_id_str']
            observed_user_ids.add(replied_to)

            replied_to_status = tweets[tweet['in_reply_to_status_id_str']]
            replied_to_status_ts = replied_to_status['created_at']
            posting_delay_sec = (utils.extract_ts_s(replied_to_status_ts) - utils.extract_ts_s(tweet_ts))#.total_seconds()
            add_edge(
                g, replier, replied_to, tweet_id, tweet_ts, 'REPLY',
                original_tweet_id=tweet['in_reply_to_status_id_str'],
                original_tweet_ts=replied_to_status_ts,
                posting_delay_sec=posting_delay_sec

            )
            # in conversation
            if tweet['in_reply_to_status_id_str'] in tweets:
                # follow the reply chain as far as we can
                conversation_root = root_of_conversation(tweet['in_reply_to_status_id_str'], tweets)
                # conversation_root MAY NOT be in the corpus - it's still a link though
                conv_root_ts = first_tweet_ts_str
                posting_delay_sec = (utils.ts_2_epoch_seconds(first_tweet_ts) - utils.extract_ts_s(tweet_ts))#.total_seconds()
                if conversation_root in tweets:
                    observed_user_ids.add(tweets[conversation_root]['user']['id_str'])
                    conv_root_ts = tweets[conversation_root]['created_at']
                    posting_delay_sec = (utils.extract_ts_s(conv_root_ts) - utils.extract_ts_s(tweet_ts))#.total_seconds()
                add_edge(
                    g, replier, conversation_root, tweet_id, tweet_ts, 'IN_CONVERSATION',
                    original_tweet_id=conversation_root,
                    original_tweet_ts=conv_root_ts,
                    posting_delay_sec=posting_delay_sec
                )
    return g


DEBUG=False
def log(msg):
    if DEBUG: eprint(msg)


if __name__ == '__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    users = {}
    communities = defaultdict(lambda: [], {})
    with open(opts.ids_file, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in csv_reader:
            r = {}
            for key in row:  # range(len(row)):
                r[key] = row[key]
            users[r['node_id']] = r
            communities[r['community_id']].append(r['node_id'])
            # users[r[0]] = r

    tweets = dict([(uid, []) for uid in users.keys()])
    earliest_ts = sys.maxsize
    latest_ts = 0
    # with open(opts.tweets_file, 'r', encoding='utf-8') as f:
    f = gzip.open(opts.tweets_file, 'rt') if opts.tweets_file[-1] in 'zZ' else open(opts.tweets_file, 'r', encoding='utf-8')
    for l in f:
        tweet = json.loads(l.strip())
        tweet['ts'] = utils.extract_ts_s(tweet['created_at']) # timestamp_2_epoch_seconds(parse_ts(tweet['created_at']))
        if tweet['ts'] < earliest_ts: earliest_ts = tweet['ts']
        if tweet['ts'] > latest_ts:   latest_ts   = tweet['ts']
        user_id = tweet['user']['id_str']
        if user_id in users.keys():
            # tweet['ts'] = timestamp_2_epoch_seconds(parse_ts(tweet['created_at']))
            tweets[user_id].append(tweet)
    f.close()
    collection_period_mins = (latest_ts - earliest_ts) / 60

    user_feature_vectors = {}
    for user_id in tweets:
        tweets[user_id].sort(key=lambda t: t['ts'])
        user_feature_vectors[user_id] = build_user_feature_vector(user_id, tweets[user_id], collection_period_mins)

    community_feature_vectors = {}
    for community_id in communities:
        community_tweets = {}
        community = communities[community_id]
        for user_id in community:
            for t in tweets[user_id]:
                community_tweets[t['id_str']] = t
            # community_tweets += tweets[user_id]
        # community_tweets.sort(key=lambda t: t['ts'])
        # build activity graph from tweets
        g = build_activity_graph(community_tweets, earliest_ts)
        # build feature vector from activity graph
        community_feature_vectors[community_id] = build_community_feature_vector(community, g)

    header = ','.join(map(str, ['Label'] + USER_FEATURES + ['U_prop_hcc_degree', 'community_id'] + COMMUNITY_FEATURES))
    print(header)
    for user_id in tweets:
        user_vector = user_feature_vectors[user_id]
        hcc_prop_degree = users[user_id]['proportional_degree']
        community_id = users[user_id]['community_id']
        community_vector = community_feature_vectors[community_id]
        print(','.join([
            opts.label,
            mk_feature_str(USER_FEATURES, user_vector),
            hcc_prop_degree,
            community_id,
            mk_feature_str(COMMUNITY_FEATURES, community_vector)
        ]))
        # print('%s: %s %s' % (user_id, str(user_feature_vectors[user_id]), str()))
