#!/usr/bin/env python3


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import networkx as nx
import os, os.path
import sys
import utils

from argparse import ArgumentParser
from mpl_toolkits.axes_grid1 import make_axes_locatable
#

MEASURES = ['JACCARD', 'OVERLAP']
class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'compare_alpha_by_window_vis.py -i <graphml dir> -o <imgfile> [opts]'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default=None,
            dest='graphml_path',
            help='The path to a directory of graphml files'
        )
        self.parser.add_argument(
            '--corpus',
            required=True,
            dest='corpus',
            help='The corpus label in the graphml files'
        )
        # self.parser.add_argument(
        #     'g_files',
        #     nargs='+',
        #     help='GraphML files to examine'
        # )
        self.parser.add_argument(
            '-o',
            dest='img_file',
            default=None,
            help='The resulting image file'
        )
        self.parser.add_argument(
            '-p', '--id-property',
            default='id',
            dest='id_key',
            help='Name of unique node property for testing equality (default: "id")'
        )
        self.parser.add_argument(
            '-s', '--sim-measure',
            choices=MEASURES,
            default=MEASURES[0],
            dest='sim_measure',
            help='The similarity measure to use (default: JACCARD)'
        )
        # self.parser.add_argument(
        #     '-l', '--labels',
        #     dest='labels',
        #     default='',
        #     help='The labels to use for each file'
        # )
        self.parser.add_argument(
            '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help='Dry run mode, does not write to disk (default: False)'
        )
        self.parser.add_argument(
            '--interactive',
            dest='interactive',
            action='store_true',
            default=False,
            help='Show plot on screen, ie. non-batch mode (default: False)'
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


def sim(g1, g2, id_attr='id', sim_measure='JACCARD'):
    # Jaccard index https://en.wikipedia.org/wiki/Jaccard_index
    g1_nodes = set([id for n, id in g1.nodes(data=id_attr)])
    g2_nodes = set([id for n, id in g2.nodes(data=id_attr)])

    in_common = len(g1_nodes.intersection(g2_nodes))
    overall = len(g1_nodes.union(g2_nodes))
    # return in_common / (overall * 1.0)
    if sim_measure == 'JACCARD':
        # https://en.wikipedia.org/wiki/Jaccard_index
        return in_common / float(overall)
    elif sim_measure == 'OVERLAP':
        # https://en.wikipedia.org/wiki/Overlap_coefficient
        return float(in_common) / min(len(g1_nodes), len(g2_nodes))
    else:
        return 0



def build_sim_mtx(gs, id_attr, sim_measure):
    mtx = []
    for r in range(len(gs)):
        mtx.append([])
        for c in range(len(gs)):
            mtx[r].append(sim(gs[r], gs[c], id_attr, sim_measure))
    return mtx


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint('[%s] %s' % (utils.now_str(), msg))


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    g_dir = opts.graphml_path

    corpus = opts.corpus
    behaviour = 'retweets' # opts.behaviour
    fsa_v_param = 0.3 # opts.fsa_v_theta
    t_param = 0.1 # opts.threshold
    alpha = '' # '-%.1f' % opts.alpha if opts.alpha else ''
    knn = 'knn'
    fsa_v = 'fsa_v_%.1f' % fsa_v_param
    threshold = 't_%.1f' % t_param
    id_key = opts.id_key
    img_file = opts.img_file
    sim_measure = opts.sim_measure

    log('building the filenames')
    def make_g_path(window, alpha):
        return os.path.join(g_dir, '%s-%s-%s%s-hccs-%s.graphml' % (corpus, behaviour, window, alpha, fsa_v))
        # return os.path.join(g_dir, '%s-%s-%s%s-hccs-%s.graphml' % (corpus, behaviour, window, alpha, method))

    A0 = ''
    A5 = '-0.5'
    A7 = '-0.7'
    A9 = '-0.9'

    a0_15m = make_g_path('15m', A0)
    a5_15m = make_g_path('15m', A5)
    a7_15m = make_g_path('15m', A7)
    a9_15m = make_g_path('15m', A9)

    a0_60m = make_g_path('60m', A0)
    a5_60m = make_g_path('60m', A5)
    a7_60m = make_g_path('60m', A7)
    a9_60m = make_g_path('60m', A9)

    a0_360m = make_g_path('360m', A0)
    a5_360m = make_g_path('360m', A5)
    a7_360m = make_g_path('360m', A7)
    a9_360m = make_g_path('360m', A9)

    a0_1440m = make_g_path('1440m', A0)
    a5_1440m = make_g_path('1440m', A5)
    a7_1440m = make_g_path('1440m', A7)
    a9_1440m = make_g_path('1440m', A9)

    log('loading the 15m graphs')
    a0_15m_g = nx.read_graphml(a0_15m)
    a5_15m_g = nx.read_graphml(a5_15m)
    a7_15m_g = nx.read_graphml(a7_15m)
    a9_15m_g = nx.read_graphml(a9_15m)

    log('loading the 60m graphs')
    a0_60m_g = nx.read_graphml(a0_60m)
    a5_60m_g = nx.read_graphml(a5_60m)
    a7_60m_g = nx.read_graphml(a7_60m)
    a9_60m_g = nx.read_graphml(a9_60m)

    log('loading the 360m graphs')
    a0_360m_g = nx.read_graphml(a0_360m)
    a5_360m_g = nx.read_graphml(a5_360m)
    a7_360m_g = nx.read_graphml(a7_360m)
    a9_360m_g = nx.read_graphml(a9_360m)

    log('loading the 1440m graphs')
    a0_1440m_g = nx.read_graphml(a0_1440m)
    a5_1440m_g = nx.read_graphml(a5_1440m)
    a7_1440m_g = nx.read_graphml(a7_1440m)
    a9_1440m_g = nx.read_graphml(a9_1440m)

    log('build 15m sim mtx')
    mtx_15m = build_sim_mtx([a0_15m_g, a5_15m_g, a7_15m_g, a9_15m_g], id_key, sim_measure)

    log('build 60m sim mtx')
    mtx_60m = build_sim_mtx([a0_60m_g, a5_60m_g, a7_60m_g, a9_60m_g], id_key, sim_measure)

    log('build 360m sim mtx')
    mtx_360m = build_sim_mtx([a0_360m_g, a5_360m_g, a7_360m_g, a9_360m_g], id_key, sim_measure)

    log('build 1400m sim mtx')
    mtx_1440m = build_sim_mtx([a0_1440m_g, a5_1440m_g, a7_1440m_g, a9_1440m_g], id_key, sim_measure)

    mtxs = [mtx_15m, mtx_60m, mtx_360m, mtx_1440m]

    # global min/max used to share colourbar across all the matrices
    global_min = min(min([min(row) for row in m]) for m in mtxs)
    global_max = max(max([max(row) for row in m]) for m in mtxs)

    def plot(fig, ax, mtx, title, colourbar=False):
        img_opts = {
            'interpolation' : 'Nearest', #'None', None will result in blurry PDFs in LaTeX docs
            'origin' : 'upper',
            'vmin' : 0, #global_min,
            'vmax' : global_max
        }
        img = ax.imshow(mtx, **img_opts)

        # getting the font sizes right took some time
        ax.set_title(title, fontsize=16)
        ax.set_xticklabels(['', '0.0', '0.5', '0.7', '0.9'], fontsize=12)
        ax.set_yticklabels(['', '0.0', '0.5', '0.7', '0.9'], fontsize=14)

        ax.xaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3]))
        ax.xaxis.set_major_formatter(plt.FixedFormatter(['0.0', '0.5', '0.7', '0.9']))

        # fix colourbar size: https://stackoverflow.com/a/18195921
        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        if not colourbar:
            # fix subplot sizing: https://stackoverflow.com/a/42397467
            cax.axis('off')
        else:
            fig.colorbar(
                img,
                ax=ax,
                # cmap='viridis',
                cax=cax
            )

    fig, (ax_15m, ax_60m, ax_360m, ax_1440m) = plt.subplots(1, 4, figsize=(10, 2.5))
    plot(fig, ax_15m, mtx_15m, '$\gamma$=15')
    plot(fig, ax_60m, mtx_60m, '$\gamma$=60')
    plot(fig, ax_360m, mtx_360m, '$\gamma$=360')
    plot(fig, ax_1440m, mtx_1440m, '$\gamma$=1440', colourbar=True)

    if opts.interactive:
        plt.show()

    if not opts.dry_run:
        plt.savefig(img_file, bbox_inches='tight', pad_inches=0)
