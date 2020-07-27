#!/usr/bin/env python3

import csv
import gzip
import sys
import utils

# Trawls through the RU-IRA dataset and counts basic statistics within a
# specified time window.

if __name__=='__main__':
    fn       = sys.argv[1]
    start_ts = utils.extract_ts_s(sys.argv[2], fmt=utils.DCW_TS_FORMAT)
    end_ts   = utils.extract_ts_s(sys.argv[3], fmt=utils.DCW_TS_FORMAT)

    try:
        if fn[-1] in 'zZ':
            in_f = gzip.open(fn, 'rt', encoding='utf-8')
        else:
            in_f = open(fn, 'r', encoding='utf-8')
        csv_reader = csv.DictReader(in_f)

        users = set()
        tweets = 0
        rts = 0
        row_count = 0
        for row in csv_reader:
            row_count = utils.log_row_count(row_count, True)
            ts = utils.extract_ts_s(row['tweet_time'], fmt=utils.IRA_TS_FORMAT)
            if ts < start_ts or ts > end_ts: continue  # may not be in timestamp order
            tweets += 1
            users.add(row['userid'])
            if row['is_retweet'].lower() == 'true': rts += 1

        print('\nTweets:   %10d' % tweets)
        print('Retweets: %10d' % rts)
        print('Accounts: %10d' % len(users))

    finally:
        in_f.close()
