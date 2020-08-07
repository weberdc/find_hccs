#!/usr/bin/env python3

import gzip
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os, os.path
import sys
import utils

from argparse import ArgumentParser

# Build account diversity ratio (# accounts / # tweets) plot.
# Based on:
# Chu Z., Widjaja I., Wang H. (2012) Detecting Social Spam Campaigns on Twitter.
# In: Bao F., Samarati P., Zhou J. (eds) Applied Cryptography and Network
# Security. ACNS 2012. Lecture Notes in Computer Science, vol 7341. Springer,
# Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-31284-7_27

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'build_adr_vis.py [options] <hcc_analysis>.json*'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            'a_files', metavar='a_file', type=str, nargs='*',
            help='JSON files of HCC analysis results'
        )
        self.parser.add_argument(
            '-o',
            default=None,
            dest='out_file',
            help='Image file to write chart to.'
        )
        self.parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            dest='dry_run',
            help='Do not write to disk (default: False)'
        )
        self.parser.add_argument(
            '-l', '--labels',
            default=None,
            dest='labels',
            required=False,
            help='Labels for the time series (label count needs to match file count) (default: filenames).'
        )
        self.parser.add_argument(
            '--legend-loc',
            default='best',
            dest='legend_loc',
            help='The location for the legend (see Matplotlib docs)'
        )
        self.parser.add_argument(
            '--iw', '--fig-width',
            default=5,
            dest='fig_width',
            type=int,
            help='Width of figure (default: 5)'
        )
        self.parser.add_argument(
            '--ih', '--fig-height',
            default=3,
            dest='fig_height',
            type=int,
            help='Height of figure (default: 3)'
        )
        self.parser.add_argument(
            '--scatter-only',
            dest='scatter',
            action='store_true',
            default=False,
            help='Scatter plot, not line (default: False)'
        )
        self.parser.add_argument(
            '--per-day',
            dest='per_day',
            action='store_true',
            default=False,
            help='Adjust ADR by number of days active, first to last post (default: False)'
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


def seconds_in_a_day():
    seconds_in_a_minute = 60
    mintues_in_an_hour = 60
    hours_in_a_day = 24
    return seconds_in_a_minute * mintues_in_an_hour * hours_in_a_day


class Styles:
    def __init__(self):
        self.current_marker = -1
        self.MARKERS = 'o^vpsPx+D.'

    def next_marker(self):
        self.current_marker += 1
        if self.current_marker >= len(self.MARKERS):
            self.current_marker = 0  # wrap
        return self.MARKERS[self.current_marker]


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    in_files = opts.a_files
    dry_run  = opts.dry_run
    img_w    = opts.fig_width
    img_h    = opts.fig_height
    img_file = opts.out_file
    leg_loc  = opts.legend_loc
    scatter  = opts.scatter
    per_day  = opts.per_day

    labels = {
        fn : lbl
        for fn, lbl
        in zip(in_files, (opts.labels.split(',') if opts.labels else in_files))
    }


    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    SECONDS_IN_A_DAY = float(seconds_in_a_day())

    adrs = {}  # list of series
    for in_file in in_files:
        in_f = utils.open_file(in_file) # gzip.open(in_file, 'rt', encoding='utf-8') if in_file[-1] in 'zZ' else open(in_file, 'r', encoding='utf-8')
        curr_adrs = []
        adrs[labels[in_file]] = curr_adrs
        for l in in_f:
            hcc_analysis = json.loads(l)
            user_count = hcc_analysis['user_count']
            tweet_count = hcc_analysis['tweet_count']
            if not per_day:
                # doesn't account for the length of the campaign
                curr_adrs.append(user_count / float(tweet_count))  # (0,1]
            else:
                tweet_tss = list(map(lambda t: t['t_ts'], hcc_analysis['tweets']))
                max_ts = max(tweet_tss) # epoch seconds
                min_ts = min(tweet_tss)
                duration_days = (max_ts - min_ts) / SECONDS_IN_A_DAY

                log('%s[%d]: %.5f days' % (labels[in_file], hcc_analysis['community_id'], duration_days))

                curr_adrs.append(user_count / float(tweet_count * duration_days))

    fig = plt.figure(figsize=(img_w, img_h))
    ax = fig.add_subplot(1,1,1)

    styles = Styles()
    max_x_value = 0
    i = 0
    for label in labels:
        curr_adrs = adrs[labels[label]]
        x_values = np.sort(curr_adrs)
        max_x_value = max(max_x_value, max(x_values))
        y_percs = 100 * np.arange(len(x_values)) / (len(x_values) - 1)

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

        if not scatter:
            ax.plot(x_values, y_percs) #, label=feature)
        ax.scatter(x_values, y_percs, marker=styles.next_marker(), alpha=0.5)
        i += 1

    # get the lines to go right up to the axes and other chart borders
    ax.set_xlim(0-max_x_value*0.05, max_x_value*1.05)
    # ax.set_ylim(0, 100)

    suffix = ' (per day active)' if per_day else ''
    ax.set_xlabel('Account diversity ratio%s' % suffix)
    ax.legend(labels.values(), loc=leg_loc)

    if dry_run:
        plt.show()
    else:
        log('Writing to %s' % img_file)
        plt.savefig(img_file, bbox_inches='tight', pad_inches=0)

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
