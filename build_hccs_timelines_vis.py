#!/usr/bin/env python3

import datetime
import DBA
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import utils

from argparse import ArgumentParser
from pandas.plotting import register_matplotlib_converters

# basic stats for a graphml file or all graphml files in a directory

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'build_hccs_timelines_vis.py -i <hcc-analysis.json>'

        self.parser = ArgumentParser(usage=usage)
        # self.parser.add_argument(
        #     '-i',
        #     default=None,
        #     dest='analysis_file',
        #     help='An HCC analysis file (JSON)'
        # )
        self.parser.add_argument(
            'hccs_files',
            nargs='+',
            help='HCCs analysis files (JSON)'
        )
        self.parser.add_argument(
            '--labels',
            dest='labels',
            default='',
            help='Labels corresponding to the HCCs analysis files'
        )
        self.parser.add_argument(
            '-o',
            dest='img_file',
            default=None,
            help='The resulting image file'
        )
        self.parser.add_argument(
            '-f', '--freq',
            dest='freq',
            default='24H',
            help='The time series bucket to use (default: 24H, see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases)'
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
            '--which',
            dest='which_hcc',
            type=int,
            default=0,
            help='The index of the HCC in the file to select (i.e., which line, default: 0)'
        )
        self.parser.add_argument(
            '--legend',
            dest='incl_legend',
            action='store_true',
            default=False,
            help='Include a legend (default: False)'
        )
        self.parser.add_argument(
            '--x-label',
            dest='x_label',
            default='',
            help='Label for the x axis (default: "")'
        )
        self.parser.add_argument(
            '--ts-label-fmt', '--x-label-fmt',
            dest='x_label_fmt',
            default='%Y-%m-%d',
            help='The timestamp format to use on the x axis (default: "%%Y-%%m-%%d")'
        )
        self.parser.add_argument(
            '--merge', '--dba',
            dest='merge',
            action='store_true',
            default=False,
            help='Merge timeseries with DBA (default: False)'
        )
        self.parser.add_argument(
            '--batch',
            dest='batch_mode',
            action='store_true',
            default=False,
            help='Batch mode - do not display plot onscreen (default: False)'
        )
        self.parser.add_argument(
            '--log',
            dest='log_y',
            action='store_true',
            default=False,
            help='Use a log scale on the y axis (default: False)'
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


def process_data_and_plot(hcc_infos, merged_hccs_label, freq, which, ax, batch_mode, dry_run):
    log('Processing %s' % merged_hccs_label)
    tweets_per_w_list = []
    communities = set()

    longest = 0
    longest_tweet_df = None
    grouped_tweets = {}
    min_ts = None
    max_ts = None
    log('Examining %d of %d HCCs' % (which, len(hcc_infos)))
    for hcc_info in hcc_infos[which:which+1]:  # just process this HCC
        c_id = hcc_info['community_id']
        communities.add(c_id)

        print(f'Tweets: {len(hcc_info["tweets"]):,}')
        series_i = [t['t_ts'] for t in hcc_info['tweets']]  # ts = seconds since epoch
        series_i.sort()
        series_i[:] = map(utils.epoch_seconds_2_ts, series_i)

        series_i = [(t['t_ts'], t['u_id']) for t in hcc_info['tweets']]
        series_i.sort(key=lambda p: p[0])
        series_i[:] = map(lambda p: (utils.epoch_seconds_2_ts(p[0]), p[1]), series_i)

        # c_tweets = pd.DataFrame([(ts, c_id) for ts in series_i], columns=['timestamp', 'community'])
        c_tweets = pd.DataFrame(series_i, columns=['timestamp', 'account'])
        tweets_grouped = c_tweets.groupby(pd.Grouper(key='timestamp', freq=freq, convention='start'))

        min_ts = min([p[0] for p in series_i])
        max_ts = max([p[0] for p in series_i])
        print(min_ts)
        print(max_ts)
        full_ts_index = pd.date_range(min_ts, max_ts, freq=freq)

        # tmp = tweets_grouped.size().reindex(index=full_ts_index, fill_value=0)
        # print(tmp.shape)
        # tmp.plot()

        series = {'All': []}
        for p in series_i:
            ts, uid = p
            if uid in series:
                series[uid].append(ts)
            else:
                series[uid] = [ts]
            series['All'].append(ts)  # aggregate
        longest = len(series['All'])
        for s in series:
            l = series[s]
            if len(l) < longest:
                series[s] = l + [np.nan] * (longest - len(l))

        new_series = { 'day_index': full_ts_index }
        for d in new_series['day_index']:
            # d = new_series['day_index'][i-1]
            next_d = d + pd.DateOffset(7) #new_series['day_index'][i]
            d_dt = datetime.datetime(*d.timetuple()[:6])
            next_d_dt = datetime.datetime(*next_d.timetuple()[:6])
            # horribly inefficient
            for s in series:
                new_series[s] = new_series.get(s, [])
                new_series[s].append(sum(
                    1 for ts in series[s]
                    if not isinstance(ts, float) and ts >= d_dt and ts < next_d_dt
                ))

        df = pd.DataFrame(new_series)
        df.set_index('day_index', inplace=True)

        months = (max_ts - min_ts).total_seconds() / (60 * 60 * 24 * 30)
        df[list(filter(lambda c: c != 'All', series.keys()))].plot(
            logy=True,
            legend=False,
            lw=1,
            ax=ax,
            ylabel=f'Tweets / {freq} (log)',
            xlabel=f'{len(hcc_info["tweets"]):,} tweets over {months:,.1f} months by {len(series.keys() - set(["All", "day_index"])):,} accounts'
        )

        if not dry_run:
            log('Writing to %s' % img_file)
            plt.savefig(img_file, bbox_inches='tight', pad_inches=0)

        if not batch_mode:
            plt.show()
        # print('exiting early...')
        # sys.exit(1)

        # # grouped_tweets[c_id] = tweets_grouped
        # grouped_tweets = tweets_grouped
        #
        # # not all HCCs will have tweeted in every window
        # # if min_ts: min_ts = min(min_ts, min(tweets_grouped.size().index))
        # # else:      min_ts = min(tweets_grouped.size().index)
        # # if max_ts: max_ts = max(max_ts, max(tweets_grouped.size().index))
        # # else:      max_ts = max(tweets_grouped.size().index)
        # min_ts = min([p[0] for p in series_i])
        # max_ts = max([p[0] for p in series_i])
        # print(min_ts)
        # print(max_ts)

    # full_ts_index = pd.date_range(min_ts, max_ts, freq=freq)
    #
    # i = 0
    # for c_id in grouped_tweets:
    #     tweets_grouped = c_id # grouped_tweets[c_id]
    #     tweets_per_w = len(tweets_grouped)#.size()
    #
    #     # fill in empty windows with zeros
    #     tweets_per_w = tweets_per_w.reindex(index=full_ts_index, fill_value=0)
    #     tweets_per_w.name = merged_labels[i] if len(merged_labels) > i else 'Account %d' % c_id
    #     i += 1
    #
    #     tweets_per_w_list.append(tweets_per_w)

    # if not opts.merge:
    #     log('Plotting the series')
    #     for tweets_per_w in tweets_per_w_list:
    #         tweets_per_w.plot()#use_index=False)
    # else:
    #     timeseries = np.array(tweets_per_w_list)
    #
    #     #calculating average series with DBA
    #     log('Performing DBA')
    #     average_series = DBA.performDBA(timeseries)
    #
    #     log('Plotting the result')
    #     plt.plot(average_series, label=merged_hccs_label)

    # return full_ts_index



DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    register_matplotlib_converters()

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    # hccs_file = opts.analysis_file
    img_w = opts.img_width
    img_h = opts.img_height
    img_file = opts.img_file
    dry_run = opts.dry_run
    freq = opts.freq
    ts_fmt = opts.x_label_fmt
    merged_labels = opts.labels.split(',')
    x_label = opts.x_label
    log_y = opts.log_y
    which_hcc = opts.which_hcc
    batch_mode = opts.batch_mode

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)


    hcc_infos = {}
    for hccs_file in opts.hccs_files:
        hcc_infos[hccs_file] = []
        with open(hccs_file, 'r', encoding='utf-8') as in_f:
            for l in in_f:
                hcc_infos[hccs_file].append(json.loads(l))

    fig, ax = plt.subplots(figsize=(img_w, img_h))

    i = 0
    min_ts = None
    max_ts = None
    hccs_file = list(hcc_infos.keys())[0]
    # for hccs_file in hcc_infos:  # accept only one file
    hccs_label = merged_labels[i] if i < len(merged_labels) else 'Series %d' % (i+1)
    # ts_index =
    process_data_and_plot(
        hcc_infos[hccs_file], hccs_label, freq, which_hcc, ax, batch_mode, dry_run
    )
    #     min_ts = ts_index[0] if not min_ts else min(min_ts, ts_index[0])
    #     max_ts = ts_index[-1] if not max_ts else max(max_ts, ts_index[-1])
    #     i += 1
    #
    # # overall timestamp range for x labels
    # ts_index = pd.date_range(min_ts, max_ts, freq=freq)
    # # plt.xticks(ts_index, map(lambda ts: ts.strftime('%Y%m%d'), ts_index))
    #
    # fig.autofmt_xdate()
    # # ax.set_xlim(left=0)
    #
    # plt.ylabel('Tweets')
    # if log_y:
    #     plt.yscale('log')
    # if x_label:
    #     plt.xlabel(x_label)
    # if opts.incl_legend:
    #     plt.legend(loc='best')
    #
    # if not dry_run:
    #     log('Writing to %s' % img_file)
    #     plt.savefig(img_file, bbox_inches='tight', pad_inches=0)
    #
    # log('displaying plot')
    # plt.show()

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
