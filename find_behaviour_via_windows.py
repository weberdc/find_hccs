#!/usr/bin/env python3

import csv
import json
import networkx as nx
import net_log_utils
import sys
import os, os.path
import utils
import find_behaviour

from argparse import ArgumentParser
# from find_behaviour import Detective
from pathlib import Path

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'find_behaviour_via_windows.py -i tweets_info.csv[.gz] -o <lcn_dir> --window <window_size> [-s|--start <timestamp>] [-e|--end <timestamp>]' # [--sliding --alpha|--fade-factor --num-windows]'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default='-',
            dest='csv_file',
            help='CSV file of tweet info in timestamp order (end filename with z for gzip)'
        )
        self.parser.add_argument(
            '-o',
            default='.',
            dest='lcn_dir',
            help='Directory for the resulting graphML files'
        )
        self.parser.add_argument(
            '-w', '--window',
            default='15m',
            dest='window_str',
            help='Window size with unit [smhd], e.g., 15m = 15 minutes, 10s = 10 seconds, 24h = 24 hours, 7d = 7 days'
        )
        # self.parser.add_argument(
        #     '-t', '--target',
        #     default='target',
        #     dest='matching_field',
        #     help='Column to use to match rows (default: "target")'
        # )
        self.parser.add_argument(
            '-t', '--targets',
            # default='target',
            required=True,
            dest='targets',
            help='Behaviours and matching columns to use to match rows, separated by pipes (e.g., "RETWEET:ot_id|MENTION:target")'
        )
        self.parser.add_argument(
            '-s', '--start',
            default='',
            dest='start_ts',
            help='Starting timestamp, e.g., 20200511_171300 (%%Y%%m%%d_%%H%%M%%S) (default: None).'
        )
        self.parser.add_argument(
            '-e', '--end',
            default='',
            dest='end_ts',
            help='Final timestamp, e.g., 20200511_171300 (%%Y%%m%%d_%%H%%M%%S) (default: None).'
        )
        # self.parser.add_argument(
        #     '-f', '--ts-format',
        #     default='%Y%m%d_%H%M%S',
        #     dest='format',
        #     help='Argument timestamp to use ([D]CW (default) or [T]witter).'
        # )
        # self.parser.add_argument(
        #     '--sliding',
        #     dest='verbose',
        #     action='store_true',
        #     default=False,
        #     help='Use sliding window (default: False)'
        # )
        self.parser.add_argument(
            '-v', '--verbose',
            dest='verbose',
            action='store_true',
            default=False,
            help='Verbose logging (default: False)'
        )
        self.parser.add_argument(
            '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help='Dry run, files will not be written (default: False)'
        )

    def parse(self, args=None):
        return self.parser.parse_args(args)


# def parse_window_cli_arg(w_str):
#     # returns window size in seconds
#     unit = w_str[-1]
#     if unit in 'sS':
#         return int(w_str[:-1])
#     elif unit in 'mM':
#         return int(w_str[:-1]) * 60
#     elif unit in 'hH':
#         return int(w_str[:-1]) * 60 * 60
#     elif unit in 'dD':
#         return int(w_str[:-1]) * 60 * 60 * 24
#     elif unit in 'wW':
#         return int(w_str[:-1]) * 60 * 60 * 24 * 7


def parse_ts_cli_arg(ts_str, fmt=utils.DCW_TS_FORMAT):
    # return ts_str as epoch seconds
    if ts_str:
        return utils.ts_2_epoch_seconds(utils.parse_ts(ts_str, fmt=fmt))
    else:
        return None


def process_batch(detector, tweets, lcn_dir, current_ts_s, t_property, w_label, dry_run):
    w_ts_str = utils.ts_to_str(current_ts_s)
    log('Processing %10d tweets in %s + %s' % (len(tweets), w_ts_str, w_label))
    if len(tweets) == 0:
        return
    lcn_file = os.path.join(lcn_dir, 'lcn-%s-%s.graphml' % (w_ts_str, w_label))
    # log('-> %s' % lcn_file)

    g = detector.gather_evidence(tweets, t_property)

    if not dry_run:
        nx.write_graphml(g, lcn_file)

    return g


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    csv_file   = opts.csv_file
    lcn_dir    = opts.lcn_dir
    dry_run    = opts.dry_run
    start_ts_s = parse_ts_cli_arg(opts.start_ts)
    end_ts_s   = parse_ts_cli_arg(opts.end_ts)
    window_s   = utils.parse_window_cli_arg(opts.window_str)
    behaviours_and_fields = find_behaviour.parse_targets_cli(opts.targets)  #{ b : t for b, t in [p.split(':') for p in opts.targets.split('|')] }

    if not dry_run:
        # https://stackoverflow.com/a/273227
        Path(lcn_dir).mkdir(parents=True, exist_ok=True)

    log_file = net_log_utils.open_log_file(lcn_dir)

    STARTING_TIME = utils.now_str()
    log('Starting at %s' % STARTING_TIME)

    log('start_ts: %s' % utils.ts_to_str(start_ts_s))
    log('end_ts:   %s' % utils.ts_to_str(end_ts_s))

    with utils.open_file(csv_file) as in_f:
        reader = csv.DictReader(in_f)
        detector = find_behaviour.Detective()

        current_window_ts_s = start_ts_s if start_ts_s else None
        batch = []
        for tweet_row in reader:
            ts = int(tweet_row['timestamp'])  # TODO: parameterise this column
            # log('Tweet time:    %d' % ts)
            # log('-> Tweet time: %s' % utils.ts_to_str(ts))
            # if not start_ts_s: start_ts_s = ts
            if not current_window_ts_s: current_window_ts_s = ts

            if ts < start_ts_s:
                # too early
                continue

            if ts > end_ts_s:
                log('Beyond the veil...')
                if batch:
                    # g = process_batch(detector, batch, lcn_dir, current_window_ts_s, opts.matching_field, opts.window_str, dry_run)
                    g = process_batch(detector, batch, lcn_dir, current_window_ts_s, behaviours_and_fields, opts.window_str, dry_run)
                    net_log_utils.log_g(current_window_ts_s, g, len(batch), log_file, dry_run)
                    batch = []
                log('Finishing... [Past %s]' % opts.end_ts)
                break

            if ts < current_window_ts_s + window_s:
                batch.append(tweet_row)

            else:  # ts in current window
                # log('Processing current batch...')
                # g = process_batch(detector, batch, lcn_dir, current_window_ts_s, opts.matching_field, opts.window_str, dry_run)
                g = process_batch(detector, batch, lcn_dir, current_window_ts_s, behaviours_and_fields, opts.window_str, dry_run)
                net_log_utils.log_g(current_window_ts_s, g, len(batch), log_file, dry_run)
                batch = []

                # log('Updating window counter...')
                # ts is now beyond the current window, so shift the window forward once
                current_window_ts_s += window_s
                # if the ts is beyond a single window, then update it again, logging empty windows
                while ts >= current_window_ts_s + window_s:
                    current_window_ts_s += window_s
                    net_log_utils.log_g(current_window_ts_s, None, 0, log_file, dry_run)

                if ts <= end_ts_s:
                    # log('Starting next window...')
                    batch.append(tweet_row)
                else:
                    log('Finishing...[No more evidence]')
                    break

        # process the last
        if batch:
            # g = process_batch(detector, batch, lcn_dir, current_window_ts_s, opts.matching_field, opts.window_str, dry_run)
            g = process_batch(detector, batch, lcn_dir, current_window_ts_s, behaviours_and_fields, opts.window_str, dry_run)
            net_log_utils.log_g(current_window_ts_s, g, len(batch), log_file, dry_run)

    log('Wrote log to %s' % log_file)
    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
