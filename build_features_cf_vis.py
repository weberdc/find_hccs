#!/usr/bin/env python3

import run_hccs_reports
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os, os.path
import sys
import utils

from argparse import ArgumentParser

# basic stats for a graphml file or all graphml files in a directory

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'build_features_cdf_vis.py -i <hcc_analysis.json>'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            required=True,
            dest='analysis_file',
            help='A JSON file of HCC analysis'
        )
        self.parser.add_argument(
            '-o',
            dest='img_file',
            default=None,
            help='The resulting image file'
        )
        self.parser.add_argument(
            '-l', '--legend-loc',
            default='best',
            dest='legend_loc',
            help='The location for the legend (see Matplotlib docs)'
        )
        self.parser.add_argument(
            '-iw', '--width',
            dest='img_width',
            type=float,
            default=4,
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


def extract_entropies(hcc_infos, feature='hashtag', skip_no_uses=True):
    entropies = []
    for hcc_info in hcc_infos:
        feat_map = hcc_info['%ss_used' % feature]
        all_uses = sum(feat_map.values())
        if skip_no_uses and all_uses == 0:
            continue
        e = run_hccs_reports.calc_entropy(run_hccs_reports.flatten_count_map(feat_map))
        entropies.append(e)

    return entropies



DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    a_file = opts.analysis_file
    dry_run = opts.dry_run
    img_file = opts.img_file
    img_w = opts.img_width
    img_h = opts.img_height
    legend_loc = opts.legend_loc

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    hcc_infos = []
    with open(a_file, 'r', encoding='utf-8') as in_f:
        for l in in_f:
            hcc_infos.append(json.loads(l))

    entropies = {
        'Hashtags' : extract_entropies(hcc_infos, 'hashtag'),
        'Domains' : extract_entropies(hcc_infos, 'domain'),
        'URLs' : extract_entropies(hcc_infos, 'url'),
        'Mentions' : extract_entropies(hcc_infos, 'mention'),
        'RTed accounts' : extract_entropies(hcc_infos, 'rt_user')
    }

    fig, ax = plt.subplots(figsize=(img_w, img_h))

    for feature in entropies:
        sorted_entropies = np.sort(entropies[feature])
        print('groups with 0 entropy for %s: %d' % (feature, sum(map(lambda v: 1, filter(lambda v: v == 0, sorted_entropies)))))
        p = 100 * np.arange(len(sorted_entropies)) / (len(sorted_entropies) - 1)

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

        ax.plot(sorted_entropies, p) #, label=feature)

        # get the lines to go right up to the axes and other chart borders
        ax.set_xlim(0, max(sorted_entropies))
        ax.set_ylim(0, 100)

    ax.set_xlabel('Entropy')
    # ax.set_ylabel('Cumulative Frequency')
    ax.legend(entropies.keys(), loc=legend_loc)

    if dry_run:
        plt.show()
    else:
        log('Writing to %s' % img_file)
        plt.savefig(img_file, bbox_inches='tight', pad_inches=0)

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
