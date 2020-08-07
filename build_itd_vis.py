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

# Build inter-arrival timing distribution plot for HCCs.
# Based on Figure 4 in:
# Chu Z., Widjaja I., Wang H. (2012) Detecting Social Spam Campaigns on Twitter.
# In: Bao F., Samarati P., Zhou J. (eds) Applied Cryptography and Network
# Security. ACNS 2012. Lecture Notes in Computer Science, vol 7341. Springer,
# Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-31284-7_27

Y_UNITS={
    'SECONDS' : 'seconds', 'S' : 'seconds',
    'MINUTES' : 'minutes', 'M' : 'minutes',
    'HOURS' : 'hours', 'H' : 'hours',
    'DAYS' : 'days', 'D' : 'days',
    'WEEKS' : 'weeks', 'W' : 'weeks'
}
DEFAULT_Y_LABEL = 'Inter-arrival distribution'
class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'build_itd_vis.py -i <hcc_analysis>.json'

        self.parser = ArgumentParser(usage=usage)
        # self.parser.add_argument(
        #     'a_files', metavar='a_file', type=str, nargs='*',
        #     help='JSON files of HCC analysis results'
        # )
        self.parser.add_argument(
            '-i',
            required=True,
            dest='in_file',
            help='HCC analysis file (JSON).'
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
            '--xl', '--x-label',
            default=None,
            dest='x_label',
            required=False,
            help='X axis label (default: None)'
        )
        self.parser.add_argument(
            '--yl', '--y-label',
            default=DEFAULT_Y_LABEL,
            dest='y_label',
            required=False,
            help='Y axis label (default: "Inter-arrival distribution")'
        )
        self.parser.add_argument(
            '--y-unit',
            default='S',
            dest='y_unit',
            choices=Y_UNITS.keys(),
            required=False,
            help='Y axis unit (options: "SECONDS|S", "MINUTES|M", "HOURS|H", "DAYS|D", "WEEKS|W")'
        )
        # self.parser.add_argument(
        #     '--legend-loc',
        #     default='best',
        #     dest='legend_loc',
        #     help='The location for the legend (see Matplotlib docs)'
        # )
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
        # self.parser.add_argument(
        #     '--scatter-only',
        #     dest='scatter',
        #     action='store_true',
        #     default=False,
        #     help='Scatter plot, not line (default: False)'
        # )
        # self.parser.add_argument(
        #     '--per-day',
        #     dest='per_day',
        #     action='store_true',
        #     default=False,
        #     help='Adjust ADR by number of days active, first to last post (default: False)'
        # )
        self.parser.add_argument(
            '-v', '--verbose',
            dest='verbose',
            action='store_true',
            default=False,
            help='Verbose logging (default: False)'
        )

    def parse(self, args=None):
        return self.parser.parse_args(args)


def seconds_in_a_unit(unit):
    seconds_in_a_minute = 60
    mintues_in_an_hour = 60
    hours_in_a_day = 24
    days_in_a_week = 7

    if unit[0] == 'S':
        return 1
    elif unit[0] == 'M':
        return seconds_in_a_minute
    elif unit[0] == 'H':
        return seconds_in_a_minute * minutes_in_an_hour
    elif unit[0] == 'D':
        return seconds_in_a_minute * mintues_in_an_hour * hours_in_a_day
    elif unit[0] == 'W':
        return seconds_in_a_minute * mintues_in_an_hour * hours_in_a_day * days_in_a_week


def unit_to_s(unit):
    return Y_UNITS[unit]


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

    in_file  = opts.in_file
    dry_run  = opts.dry_run
    img_w    = opts.fig_width
    img_h    = opts.fig_height
    img_file = opts.out_file
    x_label  = opts.x_label
    y_label  = opts.y_label
    y_unit   = opts.y_unit

    if y_label == DEFAULT_Y_LABEL:
        y_label += ' (%s)' % unit_to_s(y_unit)

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    min_ts = max_ts = None
    timelines = []  # list of timelines, each of which is a list
    with utils.open_file(in_file) as f:
        for l in f:
            hcc_analysis = json.loads(l)
            timeline = list(map(lambda t: t['t_ts'], hcc_analysis['tweets']))
            timeline.sort()
            max_ts = utils.safe_max(max_ts, timeline[-1]) # epoch seconds
            min_ts = utils.safe_min(min_ts, timeline[0])

            timelines.append(timeline)
            log('Community[%d]: %d tweets' % (hcc_analysis['community_id'], len(timeline)))

    timelines.sort(key=len, reverse=True)

    y_indices = range(0, max_ts - min_ts)
    x_indices = range(0, len(timelines))

    x_values = []
    y_values = []
    for x in x_indices:
        for ts in timelines[x]:
            x_values.append(x)
            y_values.append(ts - min_ts)

    fig = plt.figure(figsize=(img_w, img_h))
    ax = fig.add_subplot(1,1,1)

    BLACK =  '#000000'
    ax.scatter(x_values, y_values, marker='_', s=1, alpha=0.5, c=BLACK)

    if x_label: ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks([])

    ax.set_xlim(0-len(timelines)*0.01, len(timelines)*1.01)
    # ax.set_xlim(0, len(timelines))
    ax.set_ylim(0, max_ts - min_ts)

    y_unit_divisor = seconds_in_a_unit(y_unit)
    def format_y_unit(y, pos):
        return int(round(y / y_unit_divisor))
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(format_y_unit))

    # styles = Styles()
    # max_x_value = 0
    # i = 0
    # for label in labels:
    #     curr_adrs = adrs[labels[label]]
    #     x_values = np.sort(curr_adrs)
    #     max_x_value = max(max_x_value, max(x_values))
    #     y_percs = 100 * np.arange(len(x_values)) / (len(x_values) - 1)
    #
    #     ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    #
    #     if not scatter:
    #         ax.plot(x_values, y_percs) #, label=feature)
    #     ax.scatter(x_values, y_percs, marker=styles.next_marker(), alpha=0.5)
    #     i += 1
    #
    # # get the lines to go right up to the axes and other chart borders
    #
    # suffix = ' (per day active)' if per_day else ''
    # ax.set_xlabel('Account diversity ratio%s' % suffix)
    # ax.legend(labels.values(), loc=leg_loc)

    if dry_run:
        plt.show()
    else:
        log('Writing to %s' % img_file)
        plt.savefig(img_file, bbox_inches='tight', pad_inches=0)

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
