from __future__ import print_function
from datetime import datetime
from dateutil import parser


import calendar
import gzip
import json
import ntpath
import os, os.path
import sys
import time


def eprint(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, flush=True, **kwargs)


def logts(msg):
    eprint('[%s] %s' % (now_str(), msg))


def log_row_count(line_count, debug=False, lines_per_dot=100, lines_per_nl=5000):
    if debug:
        line_count += 1
        if line_count % lines_per_dot == 0: eprint('.', end='')
        if line_count % lines_per_nl  == 0: eprint(' %8d' % line_count)
    return line_count


def extract_filename(filepath, default_name='UNKNOWN.txt'):
    if not filepath:
        return default_name

    head, tail = ntpath.split(filepath)
    filename = tail or ntpath.basename(head)
    return os.path.splitext(filename)[0]


def fetch_lines(file=None, verbose=False, gz=False):
    """Gets the lines from the given file or stdin if it's None or '' or '-'."""

    def read_and_collect(lines):
        results = []
        count = 0
        for l in lines:
            if verbose:
                count += 1
                if count %  100 == 0: print('.', end='', flush=True)
                if count % 5000 == 0: print(' %8d' % count, flush=True)
            results.append(l.strip())
        return results

    if file and file != '-':
        # with open_file(file, gz) as f:
        with open_file(file) as f:
            return read_and_collect(f)  # .readlines())
    else:
        return read_and_collect(sys.stdin)


def open_file(fn):
    ### Assumes any filename ending in 'z' or 'Z' is gzipped
    return open_file_z(fn, gz=fn[-1] in 'zZ')


def open_file_z(fn, gz=False):
    if gz:
        # return gzip.open(fn, 'rb')  #, encoding='utf-8')
        # Use 'rt' https://stackoverflow.com/a/30324659
        return gzip.open(fn, 'rt')  # t for strings, not bytes
    else:
        return open(fn, 'r', encoding='utf-8')


def get_uid(t):
    return t['user']['id_str']


def get_ot_from_rt(rt):
    if 'retweeted_status' in rt:
        return rt['retweeted_status']
    else:
        return None


def is_rt(t):
    return get_ot_from_rt(t) != None


def is_qt(t):
    return 'quoted_status' in t and t['quoted_status'] != None


def is_reply(t):
    return 'in_reply_to_status_id_str' in t and t['in_reply_to_status_id_str'] != None


def flatten(list_of_lists):
    """Takes a list of lists and turns it into a list of the sub-elements"""
    return [item for sublist in list_of_lists for item in sublist]


# e.g. Tue Dec 31 06:15:21 +0000 2019
# TWITTER_TS_FORMAT='%a %b %d %H:%M:%S +0000 %Y'
TWITTER_TS_FORMAT='%a %b %d %H:%M:%S %z %Y' # BEWARE: Using %z here might screw up other code.
DCW_TS_FORMAT= '%Y%m%d_%H%M%S'  # 20110426_085755
IRA_TS_FORMAT='%Y-%m-%d %H:%M'  # 2011-04-26 08:57
IRA_SHORT_TS_FORMAT='%Y-%m-%d'  # 2011-04-26
NOW_TS_FORMAT='%Y-%m-%d %H:%M:%S'  # 2011-04-26 08:57:23


def tsver():
    """ Returns a timestamp string to the current second to use as a 'version' """
    return datetime.now().strftime(DCW_TS_FORMAT)


def parse_ts(ts_str, fmt=TWITTER_TS_FORMAT):
    time_struct = time.strptime(ts_str, fmt)
    return datetime.fromtimestamp(time.mktime(time_struct))


def ts_2_epoch_seconds(ts):
    return int(calendar.timegm(ts.timetuple()))  # GMT time
    # return int(time.mktime(ts.timetuple()))    # local time


def extract_ts_s(ts_str, fmt=TWITTER_TS_FORMAT):
    dt = parse_ts(ts_str, fmt) # parser.parse(ts_str)
    return int(calendar.timegm(dt.timetuple()))
    # return ts_2_epoch_seconds(parse_ts(ts_str, fmt))


def epoch_seconds_2_ts(ts_sec):
    return datetime.utcfromtimestamp(int(ts_sec)) # utcfrom... or from...?


def extract_ts(t, fmt=TWITTER_TS_FORMAT):
    # returns timestamp seconds since the epoch
    if 'timestamp_ms' in t:
        return int(t['timestamp_ms']) / 1000.0
    else:
        return extract_ts_s(t['created_at'], fmt)
        # return ts_2_epoch_seconds(parse_ts(t['created_at'], fmt))


def ts_to_str(ts, fmt=DCW_TS_FORMAT):
    return time.strftime(fmt, time.localtime(ts))


def now_str(fmt=NOW_TS_FORMAT):
    """ A timestamp string to the current second to use as for logging. """
    return datetime.now().strftime(fmt)


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


def lowered_hashtags_from(tweet, include_retweet=False):
    # hashtags are counted in quote tweets if they're part of the added comment
    def extract_lower_hts(entities):
        return [ht['text'].lower() for ht in entities]
    ht_entities = tweet['entities']['hashtags']
    if 'extended_tweet' in tweet:
        ht_entities = tweet['extended_tweet']['entities']['hashtags']
    hashtags = extract_lower_hts(ht_entities)
    if include_retweet and is_rt(tweet):  # 'retweeted_status' in tweet and tweet['retweeted_status']:
            hashtags += lowered_hashtags_from(get_ot_from_rt(tweet)) #['retweeted_status'])
    return hashtags


def expanded_urls_from(tweet, include_retweet=False):
    # urls are counted in quote tweets if they're part of the added comment
    url_entities = tweet['entities']['urls']
    if 'extended_tweet' in tweet:
        url_entities = tweet['extended_tweet']['entities']['urls']
    urls = [u['expanded_url'] for u in url_entities if u['expanded_url']] # skip ''
    if include_retweet and is_rt(tweet):  # 'retweeted_status' in tweet and tweet['retweeted_status']:
        urls += expanded_urls_from(get_ot_from_rt(tweet))  #['retweeted_status'])
    return urls

def mentions_from(tweet, include_retweet=False):
    m_entities = tweet['entities']['user_mentions']
    if 'extended_tweet' in tweet:
        m_entities = tweet['extended_tweet']['entities']['user_mentions']
    if include_retweet and is_rt(tweet):  #'retweeted_status' in tweet and tweet['retweeted_status']:
        m_entities += mentions_from(get_ot_from_rt(tweet))  #['retweeted_status'])
    return m_entities
    # return extract_mention_ids(m_entities)


def mentioned_ids_from(tweet, desired_field='id_str'):
    def extract_mention_ids(entities):
        return [m[desired_field] for m in entities]
    m_entities = tweet['entities']['user_mentions']
    if 'extended_tweet' in tweet:
        m_entities = tweet['extended_tweet']['entities']['user_mentions']
    return extract_mention_ids(m_entities)


def extract_domain(url, lower=False):
    url = url.lower()  # it won't matter for the domain
    header = 'https://'
    if header not in url:
        header = 'http://'
    # if header not in url:
    #     return url  # can't parse it - junk data?
    strip_http = url[url.index(header)+len(header):]
    strip_tail = strip_http[:strip_http.index('/')] if '/' in strip_http else strip_http
    if ':' in strip_tail:
        strip_tail = strip_tail[:strip_tail.index(':')]

    return strip_tail.lower() if lower else strip_tail


def extract_text(tweet):
    """Gets the full text from a tweet if it's short or long (extended)."""

    def get_available_text(t):
        if t['truncated'] and 'extended_tweet' in t:
            # if a tweet is retreived in 'compatible' mode, it may be
            # truncated _without_ the associated extended_tweet
            #eprint('#%s' % t['id_str'])
            return t['extended_tweet']['full_text']
        else:
            return t['text'] if 'text' in t else t['full_text']

    if 'retweeted_status' in tweet:
        rt = tweet['retweeted_status']
        return 'RT @%s: %s' % (rt['user']['screen_name'], extract_text(rt))

    if 'quoted_status' in tweet:
        qt = tweet['quoted_status']
        return get_available_text(tweet) + " --> " + extract_text(qt)

    return get_available_text(tweet)


def parse_window_cli_arg(w_str):
    # returns window size in seconds
    unit = w_str[-1]
    if unit in 'sS':
        return int(w_str[:-1])
    elif unit in 'mM':
        return int(w_str[:-1]) * 60
    elif unit in 'hH':
        return int(w_str[:-1]) * 60 * 60
    elif unit in 'dD':
        return int(w_str[:-1]) * 60 * 60 * 24
    elif unit in 'wW':
        return int(w_str[:-1]) * 60 * 60 * 24 * 7


def load_botornot_results(filepath):
    """Loads Botometer results into a map keyed by account ID"""
    results = {}

    for line in fetch_lines(filepath):
        result = json.loads(line)
        results[result['user']['id_str']] = result

    return results


def sort_by(l, k, reverse=False):
    return sorted(l, key=lambda i: i[k], reverse=reverse)


def sort_keys_by_vals(m, reverse=False):
    return sorted(m.keys(), key=lambda k: m[k], reverse=reverse)


def safe_max(a, b):
    if a == None: return b
    if b == None: return a
    return max(a, b)


def safe_min(a, b):
    if a == None: return b
    if b == None: return a
    return min(a, b)
