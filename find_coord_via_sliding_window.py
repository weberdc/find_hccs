#!/usr/bin/env python3

import csv
import gzip
import json
import networkx as nx
import sys
import utils

from argparse import ArgumentParser

# Searches timestamped interactions for coordination using a genuine sliding
# window

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'find_coord_via_sliding_window.py -i <interactions_file> -o <graphml filebase> -d1 <window size> -d2 <window size>'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            required=True,
            dest='interactions_file',
            help='A file of timestamped interactions'
        )
        self.parser.add_argument(
            '-o',
            required=True,
            dest='out_filebase',
            help='Filebase of where to write the LCNs to'
        )
        self.parser.add_argument(
            '-d1',
            required=True,
            dest='d1_arg',
            help='Delta 1 window size, value + unit, e.g. 10s = 10 seconds (m=mins, h=hr, d=day, w=week)'
        )
        self.parser.add_argument(
            '-d2',
            required=True,
            dest='d2_arg',
            help='Delta 2 window size, value + unit, e.g. 10s = 10 seconds (m=mins, h=hr, d=day, w=week)'
        )
        self.parser.add_argument(
            '--mode',
            dest='process_mode',
            choices=['BATCH', 'STREAM'],
            default='BATCH',
            help='Processing mode, batch or stream (default: BATCH)'
        )
        self.parser.add_argument(
            '--raw',
            dest='raw_data',
            choices=['TWEETS'],
            default=None,
            help='Expect raw JSON data objects as input (default: None)'
        )
        self.parser.add_argument(
            '--extract',
            dest='extract_what',
            choices=Extractor.EXTRACTABLES,
            default=None,
            help='What to extract from the raw JSON data objects (default: HASHTAGS)'
        )
        self.parser.add_argument(
            '--ts-col',
            default='timestamp',
            dest='timestamp_column',
            help='Name of timestamp column (default: timestamp)'
        )
        self.parser.add_argument(
            '--src-col',
            default='source',
            dest='source_column',
            help='Name of source column, i.e., potentially coordinating account (default: source)'
        )
        self.parser.add_argument(
            '--tgt-col',
            default='target',
            dest='target_column',
            help='Name of target column, i.e., value binding coordinating accounts (default: target)'
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


class Detector:

    def __init__(self, d1, d2):
        self.d1 = d1
        self.d2 = d2
        if d1 > d2:
            print(f'{d1=} can\'t be greater than {d2=}.')
            sys.exit(-1)

    def process(self, records, old_g):
        new_g = old_g #.copy()
        count = 0
        for r in records:
            count += 1
        # log(f'Processed {count} records')
        # process records
        # update old_g to new_g
        # remove whatever's needed from old_g
        return new_g



class StreamConsumer:

    def __init__(**stream_config):
        this.cfg = { **stream_config }


class BatchConsumer2:
    def __init__(self, d1=10, d2=60, ts_col='timestamp', raw_data=None, extractor=None):
        """d1=10, d2=60 in seconds"""
        if d1 > d2:
            print(f'{d1=} can\'t be greater than {d2=}.')
            sys.exit(-1)
        self.d1 = d1
        self.d2 = d2
        self.raw_data = raw_data
        self.extractor = extractor
        if self.raw_data == 'TWEETS':
            self.ts_col = 'created_at'
        else:
            self.ts_col = ts_col

    def start_processing(self, in_file):
        if in_file[-1].lower() == 'z':
            self.in_f = gzip.open(in_file, 'rb')
        else:
            self.in_f = open(in_file, 'r', encoding='utf-8')
        self.queue = []  #
        self.first_w_ts = -1
        self.done_reading = False
        self.next_line = None

    def _parse_ts(self, ts_str):
        return utils.extract_ts_s(ts_str)

    def _get_next_line(self):
        for line in self.reader:
            yield line

    def get_next_batch(self):
        # set up appropriate reader
        if self.raw_data: #== 'TWEETS':
            self.reader = self.in_f
        else:
            self.reader = csv.DictReader(self.in_f)

        if not self.next_line:
            self.next_line = self._get_next_line()

        first_iteration_this_invocation = True
        if self.raw_data == 'TWEETS':
            # increment first timestamp in window if not the first post
            log(f'{self.first_w_ts=}')
            # not the first call
            if self.first_w_ts != -1:
                self.first_w_ts += self.d1
                # dump posts that are from before the window
                new_first_idx = 0
                for post in self.queue:
                    if post['ts'] < self.first_w_ts:
                        new_first_idx += 1
                    else:
                        break
                self.queue = self.queue[new_first_idx:]

            while not self.done_reading:
            # for l in self.in_f:
                try:
                    r = next(self.next_line)
                    if self.raw_data == 'TWEETS':
                        r = json.loads(r)  # assume posts are in order
                        curr_ts = self._parse_ts(r[self.ts_col])
                    else:
                        curr_ts = int(r[self.ts_col])
                    # set first timestamp in window and first queue
                    if self.first_w_ts == -1:
                        self.first_w_ts = curr_ts
                    # fill the queue
                    if curr_ts <= self.first_w_ts + self.d2:
                        self.queue.append(self.extractor.extract(r))
                    else:
                        break
                except StopIteration:
                    break
        return self.queue



    def finish_processing(self):
        self.in_f.close()


class Extractor:
    EXTRACTABLES = ['HASHTAGS', 'URLS', 'RETWEETS', 'REPLIES', 'MENTIONS', 'QUOTES']
    def __init__(self, what):
        self.field = what

    def extract(self, post):
        pass


class TweetExtractor(Extractor):
    def __init__(self, what):
        super().__init__(what)

    def extract(self, post):
        # parse tweet
        # extract useful bits
        # return them
        pass


class BatchConsumer:
    pass


class BatchManager:
    def __init__(self, config):
        self.cfg = config
        self.raw_data = config['raw_data']
        self.csv_mode = self.raw_data == None

    def _open_file(self, in_file):
        if in_file[-1].lower() == 'z':
            return gzip.open(in_file, 'rb')
        else:
            return open(in_file, 'r', encoding='utf-8')

    def _parse_ts(self, ts_str):
        return utils.extract_ts_s(ts_str)

    def run(self):
        if self.batch_mode:
            batch_consumer = BatchConsumer()
            #     d1=self.cfg['d1'], d2=self.cfg['d2'],
            #     raw_data=self.raw_data
            # )
        if self.raw_data == 'TWEETS':
            extractor = TweetExtractor(cfg['extract_what'])
        detector = Detector(self.cfg['d1'], self.cfg['d2'])

        try:
            reader = _open_file(self.cfg['in_file'])
            if self.csv_mode:
                reader = csv.DictReader(in_f)

            start_w_ts = -1
            queue = []
            for line in reader:
                if self.raw_data == 'TWEETS':
                    t = json.loads(line)
                    if start_w_ts == -1:
                        start_w_ts = _parse_ts(t['created_at'])
                    record = extractor.process(t)
                    curr_ts = _parse_ts(t['created_at'])

                else:
                    # assume CSV
                    pass

            batch_consumer.start_processing(self.cfg['in_file'])
            print('Processing batch')
            batch = [0]
            g = nx.Graph()
            while batch:
                log('getting fresh batch')
                batch = batch_consumer.get_next_batch()
                log(f'Got fresh batch: {batch}')
                if not batch: break
                g = detector.process(batch, g)
        finally:
            batch_consumer.finish_processing()



def add_reason_node(g, r):
    g.add_node(r, label=r, _node_type='REASON')


def link_to_reason(g, n, r):
    if not g.has_edge(n, r):
        g.add_edge(n, r, weight=1.0, reason_weight=1.0, _edge_type='REASON')
    else:
        g[n][r]['weight'] += 1.0
        if 'reason_weight' not in g[n][r]:
            g[n][r]['reason_weight'] = 1.0
        else:
            g[n][r]['reason_weight'] += 1.0

def convert_to_secs(t_str):
    if t_str[-1] in 'mM':
        return int(t_str[:-1]) * 60
    elif t_str[-1] in 'hH':
        return int(t_str[:-1]) * 60 * 60
    elif t_str[-1] in 'dD':
        return int(t_str[:-1]) * 60 * 60 * 24
    elif t_str[-1] in 'wW':
        return int(t_str[:-1]) * 60 * 60 * 24 * 7
    else:
        return int(t_str[:-1]) if t_str[-1] in 'sS' else int(t_str) # seconds


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    STARTING_TIME = utils.now_str()
    log('Starting\n')

    cfg = dict(
        in_file = opts.interactions_file,
        out_filebase = opts.out_filebase,
        d1 = convert_to_secs(opts.d1_arg),
        d2 = convert_to_secs(opts.d2_arg),
        batch_mode = opts.process_mode == 'BATCH',
        raw_data = opts.raw_data,
        extract_what = opts.extract_what
    )

    if cfg['d1'] >= cfg['d2']:
        print(f'Delta 1 ({opts.d1_arg}) cannot be greater than delta 2 ({opts.d2_arg})')
        sys.exit(1)

    if opts.process_mode == 'BATCH':
        mgr = BatchManager(cfg)
        mgr.run()



    # d2_queue = []

    # in_f = gzip.open(in_file, 'rb') if in_file[-1] in 'zZ' else open(in_file, encoding='utf-8')
    # reader = csv.DictReader(in_f)
    # line_count = 0
    # for row in reader:
    #     line_count += 1
    #     if line_count % 10000:
    #         log(f'read {line_count:10,} rows')


    # g = nx.read_graphml(in_file)
    #
    # for n in g.nodes():
    #     g.nodes[n]['_node_type'] = 'ACCOUNT'
    #
    # to_add = []
    # for u, v, r_json in g.edges(data='reasons'):
    #     reasons = json.loads(r_json)
    #     for r in reasons:
    #         to_add.append( (u, v, r) )
    #
    # for u, v, r in to_add:
    #     if r not in g: add_reason_node(g, r)
    #     else: g.nodes[r]['_node_type'] = 'REASON'
    #         # g.add_node(r, label=r, _node_type='REASON')
    #     link_to_reason(g, u, r)
    #     link_to_reason(g, v, r)
    #     # if not g.has_edge(u, r):
    #     #     g.add_edge(u, r, weight=1.0, _edge_type='REASON')
    #     # else:
    #     #     g[u][r]['weight'] += 1.0
    #     # if not g.has_edge(v, r):
    #     #     g.add_edge(v, r, weight=1.0, _edge_type='REASON')
    #     # else:
    #     #     g[v][r]['weight'] += 1.0
    #
    # nx.write_graphml(g, out_file)

    log('\nFinishing, having started at %s,' % STARTING_TIME)
