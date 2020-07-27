#!/usr/bin/env python3

import csv
import json
import networkx as nx
import os, os.path
import sys
import utils

from argparse import ArgumentParser

# Decorates nodes in a network with extra attributes based on a node property

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'decorate_network.py -i <graphml file> --account-info <acct_info>.csv --bot-info <bot_info>.json'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            required=True,
            dest='graphml_file',
            help='A graphml file to decorate'
        )
        self.parser.add_argument(
            '-o',
            required=True,
            dest='out_file',
            help='Where to write the decorated graph'
        )
        self.parser.add_argument(
            '--account-info',
            default=None,
            dest='acct_info_file',
            help='A CSV file of account info for the nodes'
        )
        self.parser.add_argument(
            '--bot-info',
            default=None,
            dest='bot_info_file',
            help='A JSON file of bot info for the nodes'
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


def report_on(g_dir, g_file):
    g = nx.read_graphml(os.path.join(g_dir, g_file))
    print('%s,%d,%d,%d' % (
        utils.extract_filename(g_file), g.number_of_nodes(), g.number_of_edges(),
        nx.number_connected_components(g)
    ))


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    g_file = opts.graphml_file
    acct_info_file = opts.acct_info_file
    bot_info_file = opts.bot_info_file
    out_file = opts.out_file

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    g = nx.read_graphml(g_file)

    acct_infos = {}
    headers = []
    if acct_info_file:
        with open(acct_info_file, 'r', encoding='utf-8') as in_f:
            reader = csv.DictReader(in_f)
            headers += reader.fieldnames
            for row in reader:
                acct_infos[row['id']] = { k : row[k] for k in row }

    bot_infos = {}
    if bot_info_file:
        with open(bot_info_file, 'r', encoding='utf-8') as in_f:
            for l in in_f:
                if len(l.strip()):
                    bot_info = json.loads(l)
                    bot_infos[bot_info['user']['id_str']] = bot_info

    log('Graph: %s' % g_file)

    line_count = 0
    for n, d in g.nodes(data=True):
        line_count = utils.log_row_count(line_count, DEBUG)
        id = d['label']
        for h in headers:
            val = acct_infos[id][h] if id in acct_infos else ''
            g.nodes[n][h] = val
        if 'bot_cap_eng' not in g.nodes[n]:
            g.nodes[n]['bot_cap_eng'] = bot_infos[id]['cap']['english'] if id in bot_infos else ''
        if 'bot_cap_uni' not in g.nodes[n]:
            g.nodes[n]['bot_cap_uni'] = bot_infos[id]['cap']['universal'] if id in bot_infos else ''
        if 'bot_score_eng' not in g.nodes[n]:
            g.nodes[n]['bot_score_eng'] = bot_infos[id]['scores']['english'] if id in bot_infos else ''
        if 'bot_score_uni' not in g.nodes[n]:
            g.nodes[n]['bot_score_uni'] = bot_infos[id]['scores']['universal'] if id in bot_infos else ''

    # for n, d in g.nodes(data=True):
    #     if n == None or None in d.keys():
    #         print('n: %s (%s)\nd: %s' % (n, d['label'], d))
    #         sys.exit()

    nx.write_graphml(g, out_file)

    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
