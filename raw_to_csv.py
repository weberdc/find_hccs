#!/usr/bin/env python3

import csv
import gzip
import json
import re
import sys
import utils

from argparse import ArgumentParser


TOPICS = [
  'RETWEET', 'RETWEETS',
  'HASHTAG', 'HASHTAGS', 'ALL_HASHTAGS',
  'URL', 'URLS', 'ALL_URLS',
  'POST_URL', 'POST_URLS', 'ALL_POST_URLS',
  'DOMAIN', 'DOMAINS', 'ALL_DOMAINS',
  'MENTION', 'MENTIONS', 'ALL_MENTIONS',
  'REPLY', 'REPLIES',
  'TIMESTAMP', 'TIMESTAMPS', 'TS'
]
class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'raw_to_csv.py -i tweets_file.json[l|.gz] -o relevant_info.csv --topic <topic>'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default='-',
            dest='tweets_file',
            help='File of tweets, if relevant, one JSON object per line ("-" for stdin, end filename with z for gzip)'
        )
        self.parser.add_argument(
            '-o',
            default='-',
            dest='csv_file',
            help='Relevant parts of tweets as CSV'
        )
        self.parser.add_argument(
            '--topic',
            choices=TOPICS,
            dest='topic',
            help='Determines the info to extract'
        )
        self.parser.add_argument(
            '--ira',
            dest='ira',
            action='store_true',
            default=False,
            help='Expect Twitter\'s IRA dataset (default: False)'
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


def write_header(f, topic):
    if topic in ['RETWEET', 'RETWEETS', 'REPLY', 'REPLIES']:
        f.write('timestamp,source,target,interaction,rt_id,ot_id\n')
    elif topic in ['MENTION', 'MENTIONS']:
        f.write('timestamp,source,target,interaction,t_id,mentioned_screen_name\n')
    elif topic == 'ALL_MENTIONS':
        f.write('timestamp,source,target,interaction,t_id,mentioned_screen_names\n')
    elif topic in ['TIMESTAMP', 'TIMESTAMPS', 'TS']:
        f.write('timestamp,source,t_id\n')
    else:  #if topic in list(set(TOPICS) - set(['RETWEET', 'MENTION', 'REPLY'])):
        f.write('timestamp,source,target,interaction,t_id\n')


def check_url(url):
    return len(url) >= 4 and url[:4] == 'http'
    # if 'http' not in url:
    #     utils.eprint('URL in tweet [%s] is invalid: %s' % (t_id, url))
    #     return False
    # else:
    #     return True


def write_url_row(csv_f, topic, url, ts, source, t_id):
    if 'http' not in url:
        utils.eprint('URL in tweet [%s] is invalid: %s' % (t_id, url))
        return False

    if topic in ['URL', 'URLS'] and not TWEET_URL_REGEX.match(url):
        csv_f.writerow([ts, source, url, 'URL', t_id])
    elif topic == 'ALL_URLS':
        csv_f.writerow([ts, source, url, 'URL', t_id])
    elif topic in ['DOMAIN', 'DOMAINS'] and not TWEET_URL_REGEX.match(url):
        csv_f.writerow([ts, source, utils.extract_domain(url), 'DOMAIN', t_id])
    elif topic == 'ALL_DOMAINS':
        csv_f.writerow([ts, source, utils.extract_domain(url), 'DOMAIN', t_id])
    elif topic in ['ALL_POST_URLS', 'POST_URL', 'POST_URLS']:
        # NB POST URLs will miss fb.com/story.php?storyID
        if topic in ['POST_URL', 'POST_URLS'] and TWEET_URL_REGEX.match(url):
            return
        post_url = url[:url.index('?')] if '?' in url else url
        csv_f.writerow([ts, source, post_url, 'URL', t_id])

    return True  # success


TWEET_URL_REGEX = re.compile('https://twitter.com/[^/]*/status/.*')
def write_rows_from_tweet(csv_f, t, topic):
    global REPLY_COUNT  # declare that we want to change REPLY_COUNT
    ts = utils.extract_ts_s(t['created_at'])
    t_id = t['id_str']
    source = utils.get_uid(t)
    if topic in ['RETWEET', 'RETWEETS'] and utils.is_rt(t):
        ot = utils.get_ot_from_rt(t)
        target = utils.get_uid(ot)
        rt_id = t_id
        ot_id = utils.get_ot_from_rt(t)['id_str']
        csv_f.writerow([ts, source, target, 'RETWEET', rt_id, ot_id])
    elif topic in ['REPLY', 'REPLIES']:
        target = t['in_reply_to_user_id_str']
        ot_id  = t['in_reply_to_status_id_str']
        if target and ot_id:
            csv_f.writerow([ts, source, target, 'REPLY', t_id, ot_id])
    elif topic in ['HASHTAG', 'HASHTAGS', 'ALL_HASHTAGS']:
        hashtags = utils.lowered_hashtags_from(t, include_retweet=True)
        if is_empty(hashtags):
            return
        if topic == 'ALL_HASHTAGS':
            csv_f.writerow([ts, source, ' '.join(hashtags), 'ALL_HASHTAGS', t_id])
        else:
            for ht in hashtags:
                csv_f.writerow([ts, source, ht, 'HASHTAG', t_id])
    elif topic in ['URL', 'URLS', 'POST_URL', 'POST_URLS', 'ALL_URLS', 'ALL_POST_URLS', 'DOMAIN', 'DOMAINS', 'ALL_DOMAINS']:
        for url in set(utils.expanded_urls_from(t, include_retweet=True)):
            write_url_row(csv_f, topic, url, ts, source, t_id)
    elif topic in ['MENTION', 'MENTIONS', 'ALL_MENTIONS']:
        mention_objs = utils.mentions_from(t, include_retweet=True)
        if is_empty(mention_objs):
            return
        if topic == 'ALL_MENTIONS':
            mentioned_ids_str = ' '.join([m['id_str'] for m in mention_objs])
            mentioned_sns_str = ' '.join([m['screen_name'] for m in mention_objs])
            csv_f.writerow([ts, source, mentioned_ids_str, 'ALL_MENTIONS', t_id, mentioned_sns_str])
        else:
            for m in mention_objs:
                csv_f.writerow([ts, source, m['id_str'], 'MENTION', t_id, m['screen_name']])
    elif topic in ['TIMESTAMP', 'TIMESTAMPS', 'TS']:
        csv_f.writerow([ts, source, t_id])


def parse_ira_hashtags(hts_str):
    if not hts_str or hts_str == '[]': return []
    # e.g., [NightmareonElmStreet, SanAntonio, Halloween, FreddyKrueger]
    return list(map(lambda s: s.strip().lower(), hts_str[1:-1].split(',')))


def parse_ira_urls(urls_str):
    if not urls_str or urls_str == '[]': return []
    # e.g., [https://goo.gl/mDoZ16]
    return list(map(lambda s: s.strip(), urls_str[1:-1].split(',')))


def parse_ira_mentions(mentions_str):
    if not mentions_str or mentions_str == '[]': return []
    # e.g., [1234,4567,7890]
    return list(map(lambda s: s.strip(), mentions_str[1:-1].split(',')))


def write_rows_from_ira_row(csv_f, r, topic):
    ts = utils.extract_ts_s(r['tweet_time'], fmt=utils.IRA_TS_FORMAT)
    t_id = r['tweetid']
    source = r['userid']
    if topic in ['RETWEET', 'RETWEETS'] and r['is_retweet'] == 'true':
        target = r['retweet_userid']
        rt_id = r['tweetid']
        ot_id = r['retweet_tweetid']
        csv_f.writerow([ts, source, target, 'RETWEET', rt_id, ot_id])
    elif topic in ['REPLY', 'REPLIES']:
        target = r['in_reply_to_userid']
        ot_id  = r['in_reply_to_tweetid']
        if target and ot_id:
            csv_f.writerow([ts, source, target, 'REPLY', t_id, ot_id])
    elif topic in ['HASHTAG', 'HASHTAGS', 'ALL_HASHTAGS']:
        hashtags = parse_ira_hashtags(r['hashtags'])
        if is_empty(hashtags):
            return
        if topic == 'ALL_HASHTAGS':
            csv_f.writerow([ts, source, ' '.join(hashtags), 'HASHTAG', t_id])
        else:
            for ht in hashtags:
                csv_f.writerow([ts, source, ht, 'HASHTAG', t_id])
    elif topic in ['URL', 'URLS', 'POST_URL', 'POST_URLS', 'ALL_URLS', 'ALL_POST_URLS', 'DOMAIN', 'DOMAINS', 'ALL_DOMAINS']:
        # some of the URLs in the RU-IRA dataset are a bit wonky
        urls = set(parse_ira_urls(r['urls']))
        success = True
        for u in urls:
            success = success and check_url(u)
        if success:
            for url in set(parse_ira_urls(r['urls'])):
                write_url_row(csv_f, topic, url, ts, source, t_id)
        else:
            # strip spurious commas
            write_url_row(csv_f, topic, ''.join(urls), ts, source, t_id)
    elif topic in ['MENTION', 'MENTIONS', 'ALL_MENTIONS']:
        mention_ids = parse_ira_mentions(r['user_mentions'])
        if is_empty(mention_ids):
            return
        if topic == 'ALL_MENTIONS':
            m_ids_str = ' '.join(mention_ids)
            csv_f.writerow([ts, source, m_ids_str, 'MENTION', t_id, m_ids_str])
        else:
            for m_id in mention_ids:
                csv_f.writerow([ts, source, m_id, 'MENTION', t_id, m_id])
    elif topic in ['TIMESTAMP', 'TIMESTAMPS', 'TS']:
        csv_f.writerow([ts, source, t_id])


def is_empty(l):
    return l == None or len(l) == 0


DEBUG=False
def log(msg=None):
    if DEBUG: utils.logts(msg) if msg else utils.eprint()


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    STARTING_TIME = utils.now_str()
    log('Starting at %s' % STARTING_TIME)


    tweets_file = opts.tweets_file
    csv_file = opts.csv_file
    topic = opts.topic
    ira = opts.ira

    log('Extracting %s from %s' % (topic, tweets_file))

    with open(csv_file, mode='w', newline='\n', encoding='utf-8') as out_f:
        write_header(out_f, topic)
        csv_writer = csv.writer(out_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        in_f = gzip.open(tweets_file, 'rt', encoding='utf-8') if tweets_file[-1] in 'zZ' else open(tweets_file, 'r', encoding='utf-8')
        line_count = 0
        if ira:
            csv_reader = csv.DictReader(in_f)
            for row in csv_reader:
                line_count = utils.log_row_count(line_count, DEBUG)
                write_rows_from_ira_row(csv_writer, row, topic)
        else:
            for l in in_f:
                line_count = utils.log_row_count(line_count, DEBUG)
                t = json.loads(l)
                write_rows_from_tweet(csv_writer, t, topic)

    log()
    log('Wrote to %s' % csv_file)

    log('Having started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
