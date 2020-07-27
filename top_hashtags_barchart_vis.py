#!/usr/bin/env python3


import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import networkx as nx
import numpy as np
import os, os.path
import sys
import utils

from argparse import ArgumentParser
from mpl_toolkits.axes_grid1 import make_axes_locatable
#

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'compare_alpha_by_window_vis.py -o <imgfile> -i <graphml dir>'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default=None,
            dest='analyses_file',
            help='The path to a JSON HCC analysis file'
        )
        self.parser.add_argument(
            '--corpus',
            default=None,
            dest='corpus',
            help='The corpus label in the graphml files'
        )
        # self.parser.add_argument(
        #     'g_files',
        #     nargs='+',
        #     help='GraphML files to examine'
        # )
        self.parser.add_argument(
            '-o',
            dest='img_file',
            default=None,
            help='The resulting image file'
        )
        self.parser.add_argument(
            '-iw', '--width',
            dest='img_width',
            type=float,
            default=6,
            help='The width of the image (default: 6)'
        )
        self.parser.add_argument(
            '-ih', '--height',
            dest='img_height',
            type=float,
            default=4,
            help='The height of the image (default: 4)'
        )
        self.parser.add_argument(
            '--top-x-hashtags',
            dest='top_x_hts',
            type=int,
            default=10,
            help='The top x hashtags to consider (default: 10)'
        )
        self.parser.add_argument(
            '--top-x-hccs',
            dest='top_x_hccs',
            type=int,
            default=10,
            help='The largest x HCCs to consider (default: 10)'
        )
        self.parser.add_argument(
            '--max-hashtags',
            dest='max_hts',
            type=int,
            default=10,
            help='The most hashtags to plot (default: 10)'
        )
        self.parser.add_argument(
            '--log',
            dest='log_x',
            action='store_true',
            default=False,
            help='Use log scale on the x axis (default: False)'
        )
        self.parser.add_argument(
            '--normalise',
            dest='normalise',
            action='store_true',
            default=False,
            help='Normalise hashtag uses by the number of users/accounts (default: False)'
        )
        self.parser.add_argument(
            '--redact',
            dest='redactions',
            default='',
            help='Hashtags to redact, comma separated'
        )
        # self.parser.add_argument(
        #     '-p', '--id-property',
        #     default='id',
        #     dest='id_key',
        #     help='Name of unique node property for testing equality (default: "id")'
        # )
        # self.parser.add_argument(
        #     '-l', '--labels',
        #     dest='labels',
        #     default='',
        #     help='The labels to use for each file'
        # )
        self.parser.add_argument(
            '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help='Dry run mode, does not write to disk (default: False)'
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


def sort_by_size(m, asc=True):
    return sorted([(k, v) for k, v in m.items()], key=lambda p: p[1], reverse=not asc)


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    # g_dir = opts.graphml_path
    anal_file = opts.analyses_file

    corpus = opts.corpus
    behaviour = 'retweets' # opts.behaviour
    fsa_v_param = 0.3 # opts.fsa_v_theta
    t_param = 0.1 # opts.threshold
    alpha = '' # '-%.1f' % opts.alpha if opts.alpha else ''
    knn = 'knn'
    fsa_v = 'fsa_v_%.1f' % fsa_v_param
    threshold = 't_%.1f' % t_param
    # id_key = opts.id_key
    img_file = opts.img_file
    img_w = opts.img_width
    img_h = opts.img_height
    top_x_hts = opts.top_x_hts
    top_x_hccs = opts.top_x_hccs
    max_hts = opts.max_hts
    log_x = opts.log_x
    normalise = opts.normalise
    redactions = opts.redactions.split(',')

    top_hashtags_by_hcc = {}
    hcc_sizes = {}
    hcc_t_counts = {}
    with open(anal_file, 'r', encoding='utf-8') as in_f:
        for l in in_f:
            analysis = json.loads(l)
            c_id = analysis['community_id']
            hcc_sizes[c_id] = analysis['user_count']
            hcc_t_counts[c_id] = analysis['tweet_count']
            top_hashtags_by_hcc[c_id] = {
                ht : c / (hcc_sizes[c_id] if normalise else 1)
                for ht, c in [
                    (ht, c) for ht, c in
                    sort_by_size(analysis['hashtags_used'], asc=False)
                ][:top_x_hts]
            }

    largest_hccs = sort_by_size(hcc_t_counts, asc=False)[:top_x_hccs]

    log('num hccs: %d' % len(largest_hccs))
    all_hashtags = {}  # ht : overall_count
    for (c_id, c_size) in largest_hccs:
        log('%d: hashtags: %s' % (c_id, str(top_hashtags_by_hcc[c_id])))
        for ht in top_hashtags_by_hcc[c_id]:
            if ht not in all_hashtags: all_hashtags[ht] = 0
            all_hashtags[ht] += (top_hashtags_by_hcc[c_id][ht] / hcc_sizes[c_id] if normalise else 1)

    log('all_hashtags: %d' % len(all_hashtags))

    if len(all_hashtags) > max_hts:
        top_10 = sort_by_size(all_hashtags, asc=False)[:max_hts]
        all_hashtags = { ht : c for ht, c in top_10 }

    log(top_hashtags_by_hcc[0])
    ht_vectors = {}
    for i in range(len(largest_hccs)):
        (c_id, c_size) = largest_hccs[i]
        c_hts = [top_hashtags_by_hcc[c_id].get(ht, 0) for ht in all_hashtags]
        ht_vectors[c_id] = c_hts

    print('HCC_id,%s' % ','.join(all_hashtags.keys()))
    for c_id in ht_vectors:
        print('%s,%s' % (c_id, ','.join(map(str, ht_vectors[c_id]))))

    fix, ax = plt.subplots(figsize=(img_w, img_h))
    bar_width = 1 / (top_x_hccs + 1)  # 0.35
    opacity = 0.8

    indices = np.arange(len(all_hashtags))
    for i in range(len(largest_hccs)):
        (c_id, t_count) = largest_hccs[i]
        c_size = hcc_sizes[c_id]
        plt.barh(indices + i * bar_width, ht_vectors[c_id], bar_width, label='%d (%d)' % (c_size, t_count))

    def redact(hts):
        return [
            ht if ht[1:] not in redactions else 'REDACTED'
            for ht
            in hts
        ]

    plt.yticks(indices + bar_width / 2, list(redact(map(lambda ht: '#%s' % ht, all_hashtags.keys()))))
    if log_x:
        ax.set_xscale('log')
    plt.legend(loc='best')
    if normalise:
        ax.set_xlabel('Hashtag uses per account')

    plt.tight_layout()
    if opts.dry_run:
        plt.show()
    else:
        log('Writing to %s' % img_file)
        plt.savefig(img_file, bbox_inches='tight', pad_inches=0)

    log('Done')
