#!/usr/bin/env python3

import json
import math
import nltk
import numpy as np
import re
import sys
import utils

from argparse import ArgumentParser

# Builds reports on HCCs from the info extracted by interrogate_hccs.py

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'analyse_hccs.py -i <hccs_info>.json'  # [-o <report>.csv]'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i', '--hccs-info',
            required=True,
            dest='hccs_info_file',
            help='JSON file of relevant HCC info'
        )
        self.parser.add_argument(
            '-o',
            required=True,
            dest='out_file',
            help='CSV file to write report to'
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


def flatten_count_map(c_map):
    labels = []
    for k in c_map:
        count = c_map[k]
        labels += [k] * count
    return labels


def calc_entropy(labels):
    """ Computes entropy of label distribution. """
    # from https://stackoverflow.com/a/45091961

    n_labels = len(labels)

    if n_labels <= 1:
        return 0

    value,counts = np.unique(labels, return_counts=True)
    probs = counts / n_labels
    n_classes = np.count_nonzero(probs)

    if n_classes <= 1:
        return 0

    ent = 0.0

    # Compute entropy
    base = math.e #if base is None else base
    for i in probs:
        ent -= i * math.log(i, base)

    return ent


def report_on_features(hcc_infos, out_f, feature='hashtag', top_k=5, f_is_special=lambda f, hcc_info: False):
    report = 'Community ID,Most used %ss,All %s uses,Tweets,Accounts\n' % (feature, feature)
    for hcc_info in utils.sort_by(hcc_infos, 'community_id'):
        c_id = hcc_info['community_id']
        feat_map = hcc_info['%ss_used' % feature]
        all_uses = sum(feat_map.values())
        account_count = hcc_info['user_count']
        tweet_count = len(hcc_info['tweets'])
        feat_strs = []
        for feat_val in utils.sort_keys_by_vals(feat_map, reverse=True):
            special_flag = '*' if f_is_special(feat_val, hcc_info) else ''
            feat_strs.append('%s%s(%d)' % (feat_val, special_flag, feat_map[feat_val]))
        most_used = ' '.join(feat_strs[:top_k])
        report += '%s,%s,%d,%d,%d\n' % (c_id, most_used, all_uses, tweet_count, account_count)
        # print('c[%d]: %s' % (c_id, ', '.join(hcc_info['tweets_by_users'].keys())))
    out_f.write(report + '\n')


def report_on_feature_diversity(hcc_infos, out_f, feature='hashtag'):
    report = 'Commmunity ID,Unique %ss,%ss Uses,Tweets,Accounts,Feature Diversity,Feature/Tweet Diversity,Feature Entropy\n' % (feature, feature)
    for hcc_info in utils.sort_by(hcc_infos, 'community_id'):
        c_id = hcc_info['community_id']
        account_count = hcc_info['user_count']
        tweet_count = len(hcc_info['tweets'])
        feat_map = hcc_info['%ss_used' % feature]
        all_uses = sum(feat_map.values())
        f_div = len(feat_map.keys()) / float(all_uses) if all_uses else 0.0
        f_t_div = f_div / tweet_count
        entropy = calc_entropy(flatten_count_map(feat_map))
        report += '%s\n' % ','.join([
            '%s' % c_id, '%d' % len(feat_map.keys()), '%d' % all_uses,
            '%d' % tweet_count, '%d' % account_count,
            '%f' % f_div, '%f' % f_t_div, '%f' % entropy
        ])
    out_f.write(report + '\n')


def report_on_int_ext_feature_diversity(hcc_infos, out_f):
    report = 'Community ID,Accounts,Tweets,RTed users,Int. RTed users,Ext. RTed users,Int/All RTed Users,RTs,Int. RTs,Ext. RTs,Int/All RTs\n'
    for hcc_info in utils.sort_by(hcc_infos, 'community_id'):
        c_id = hcc_info['community_id']
        account_count = hcc_info['user_count']
        tweet_count = len(hcc_info['tweets'])
        rted_map = hcc_info['rt_users_used']
        int_rted_map = hcc_info['int_rt_users_used']
        ext_rted_map = { id : c for id, c in rted_map.items() if id not in int_rted_map }
        int_all_rted_users = (len(int_rted_map) / float(len(rted_map))) if len(rted_map) else 0
        rt_count = hcc_info['rt_t_count']
        int_rt_count = hcc_info['int_rt_t_count']
        ext_rt_count = rt_count - int_rt_count
        int_all_rts = (int_rt_count / float(rt_count)) if rt_count else 0

        report += '%s\n' % ','.join([
            '%s' % c_id, '%d' % account_count, '%d' % tweet_count,
            '%d' % len(rted_map), '%d' % len(int_rted_map), '%d' % len(ext_rted_map), '%f' % int_all_rted_users,
            '%d' % rt_count, '%d' % int_rt_count, '%d' % ext_rt_count, '%f' % int_all_rts
        ])
    out_f.write(report + '\n')

    report = 'Community ID,Accounts,Tweets,Mentioned users,Int. mentioned users,Ext. mentioned users,Int/All mentioned Users,Mentions,Int. mentions,Ext. mentions,Int/All mentions\n'
    for hcc_info in utils.sort_by(hcc_infos, 'community_id'):
        c_id = hcc_info['community_id']
        account_count = hcc_info['user_count']
        tweet_count = len(hcc_info['tweets'])
        m_map = hcc_info['mentions_used']
        int_m_map = { id : c for id, c in m_map.items() if id in hcc_info['users'] }
        ext_m_map = { id : c for id, c in m_map.items() if id not in int_m_map }
        # int_rted_map = hcc_info['int_rt_users_used']
        int_all_m_users = (len(int_m_map) / float(len(m_map))) if len(m_map) else 0
        m_count = sum(m_map.values())   #hcc_info['rt_t_count']
        int_m_count = sum(int_m_map.values())  # hcc_info['int_rt_t_count']
        ext_m_count = m_count - int_m_count
        int_all_ms = (int_m_count / float(m_count)) if m_count else 0

        report += '%s\n' % ','.join([
            '%s' % c_id, '%d' % account_count, '%d' % tweet_count,
            '%d' % len(m_map), '%d' % len(int_m_map), '%d' % len(ext_m_map), '%f' % int_all_m_users,
            '%d' % m_count, '%d' % int_m_count, '%d' % ext_m_count, '%f' % int_all_ms
        ])
    out_f.write(report + '\n')


def report_on_content_diversity(kcc_infos, out_f, n=5):
    pass
    # for hcc_info in sort_by(hcc_infos, 'community_id'):
    #     tweets = hcc_info['tweets']
    #     for t in tweets:
    #         text = t['text']
    #         five_grams = nltk.ngrams(t['text'].split())


def report_on_temporal_diversity(kcc_infos, out_f):
    pass


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    out_file = opts.out_file

    STARTING_TIME = utils.now_str()
    log('Starting at %s' % STARTING_TIME)

    # open info file
    hcc_infos = []
    with open(opts.hccs_info_file, 'r', encoding='utf-8') as f_in:
        for l in f_in:
            hcc_infos.append(json.loads(l))

    def is_internal_acct_id(m_id, hcc):
        # test if an account ID is of an HCC member
        hcc_users = hcc['tweets_by_users']
        return m_id in hcc_users

    with open(out_file, 'w', encoding='utf-8') as out_f:
        # most used features
        report_on_features(hcc_infos, out_f, feature='hashtag', top_k=10)
        report_on_features(hcc_infos, out_f, feature='domain', top_k=10)
        report_on_features(hcc_infos, out_f, feature='url', top_k=10)
        report_on_features(
            hcc_infos, out_f, feature='mention', top_k=10,
            f_is_special=is_internal_acct_id
        )

        # diversity measure of URLs, domains, hashtags, mentions, retweeted users
        report_on_feature_diversity(hcc_infos, out_f, feature='hashtag')
        report_on_feature_diversity(hcc_infos, out_f, feature='domain')
        report_on_feature_diversity(hcc_infos, out_f, feature='url')
        report_on_feature_diversity(hcc_infos, out_f, feature='mention')
        report_on_feature_diversity(hcc_infos, out_f, feature='rt_user')

        # internal vs external retweeting/mentioning
        report_on_int_ext_feature_diversity(hcc_infos, out_f)

        # n-gram analysis
        report_on_content_diversity(hcc_infos, out_f)

        # temporal diversity
        report_on_temporal_diversity(hcc_infos, out_f)

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
