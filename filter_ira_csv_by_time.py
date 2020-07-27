#!/usr/bin/env python3

import argparse
import csv
import sys
import time

from datetime import datetime


def parse_args(args):
    parser = argparse.ArgumentParser(description='Filter IRA-formatted CSV')
    parser.add_argument(
        '--header', default=False, action='store_true', dest='header',
        help='Expect a header row in the input'
    )
    parser.add_argument(
        '--write-header', default=False, action='store_true', dest='write_header',
        help='Write a header row in the output'
    )
    parser.add_argument(
        '--input-is-ordered', default=False, action='store_true', dest='ordered',
        help='Expects the input to be ordered already'
    )
    parser.add_argument(
        '-i', '--in-file', required=True, dest='in_file',
        help='Input CSV file.'
    )
    parser.add_argument(
        '-o', '--out-file', required=True, dest='out_file',
        help='Output CSV file.'
    )
    parser.add_argument(
        '-s', '--start', default='', dest='start_ts',
        help='Starting timestamp, format %Y%m%d_%H%M%S (default: None).'
    )
    parser.add_argument(
        '-e', '--end', default='', dest='end_ts',
        help='Final timestamp, format %Y%m%d_%H%M%S (default: None).'
    )
    # parser.add_argument(
    #     '-f', '--arg-format', default='%Y%m%d_%H%M%S', dest='format',
    #     help='Argument timestamp to use ([D]CW (default) or [T]witter).'
    # )
    return parser.parse_args(args)


FIELDNAMES=[
    "tweetid",
    "userid",
    "user_display_name",
    "user_screen_name",
    "user_reported_location",
    "user_profile_description",
    "user_profile_url",
    "follower_count",
    "following_count",
    "account_creation_date",
    "account_language",
    "tweet_language",
    "tweet_text",
    "tweet_time",
    "tweet_client_name",
    "in_reply_to_tweetid",
    "in_reply_to_userid",
    "quoted_tweet_tweetid",
    "is_retweet",
    "retweet_userid",
    "retweet_tweetid",
    "latitude",
    "longitude",
    "quote_count",
    "reply_count",
    "like_count",
    "retweet_count",
    "hashtags",
    "urls",
    "user_mentions",
    "poll_choices"
]

def conv_to_ts(ts_str, infmt):
    time_struct = time.strptime(ts_str, infmt)
    return datetime.fromtimestamp(time.mktime(time_struct))

if __name__=='__main__':
    opts = parse_args(sys.argv[1:])

    IRA_TS_FORMAT = '%Y-%m-%d %H:%M'
    # IRA_DATE_FORMAT = '%Y-%m-%d'
    # TWITTER_TS_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'  #Tue Apr 26 08:57:55 +0000 2011
    ARG_FORMAT = '%Y%m%d_%H%M%S'  # 20110426_085755

    start_ts = conv_to_ts(opts.start_ts, ARG_FORMAT)
    end_ts   = conv_to_ts(opts.end_ts, ARG_FORMAT)

    print('Keeping tweets from %s to %s' % (start_ts, end_ts))

    print('Reading to %s' % opts.in_file)
    matching_rows = {} # (tweet ID, ts) : tweet line
    count = 0
    # look through all lines
    with open(opts.in_file, 'r', newline='', encoding='utf-8') as in_f:
        reader = csv.DictReader(in_f, fieldnames=FIELDNAMES) if not opts.header else csv.DictReader(in_f)
        for row in reader:
            t_id = row['tweetid']
            ts = conv_to_ts(row['tweet_time'], IRA_TS_FORMAT)

            # keep the rows that match
            if ts >= start_ts and ts <= end_ts:
                matching_rows[(t_id, ts)] = row

            if opts.ordered and ts > end_ts:
                break
            count += 1
            if count % 10000 == 0:
                print('Read: %10d' % count)

    print('Found %d matches in %d rows' % (len(matching_rows), count))
    print('Writing to %s' % opts.out_file)

    sorted_keys = sorted(matching_rows.keys(), key=lambda k: k[1])
    with open(opts.out_file, 'w', newline='', encoding='utf-8') as out_f:
        writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, quoting=csv.QUOTE_ALL)

        if opts.write_header:
            writer.writeheader()
        for k in sorted_keys:
            writer.writerow(matching_rows[k])

    print('DONE')
            # sort them and write them out.
