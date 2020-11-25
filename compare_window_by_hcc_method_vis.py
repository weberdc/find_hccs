#!/usr/bin/env python3


import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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
        usage = 'compare_window_by_hcc_method_vis.py -o <imgfile> -i <graphml dir>'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            default=None,
            dest='graphml_path',
            help='The path to a directory of graphml files'
        )
        self.parser.add_argument(
            '--corpus',
            default=None,
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


def sim(g1, g2, sim_measure='JACCARD', id_attr='id'):
    g1_nodes = set([id for n, id in g1.nodes(data=id_attr)])
    g2_nodes = set([id for n, id in g2.nodes(data=id_attr)])

    in_common = len(g1_nodes.intersection(g2_nodes))
    overall = len(g1_nodes.union(g2_nodes))

    if sim_measure == 'JACCARD':
        # https://en.wikipedia.org/wiki/Jaccard_index
        return in_common / float(overall)
    elif sim_measure == 'OVERLAP':
        # https://en.wikipedia.org/wiki/Overlap_coefficient
        return float(in_common) / min(len(g1_nodes), len(g2_nodes))
    else:
        return 0


def build_sim_mtx(gs, id_attr, sim_measure):
    mtx = [[] for i in range(len(gs))]
    for r in range(len(gs) - 1, -1, -1):  # gs[0] x gs[0] in bottom left corner
        # mtx.append([])
        for c in range(len(gs)):
            mtx[r].append(sim(gs[len(gs) - r - 1], gs[c], sim_measure, id_attr))
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
    def make_g_path(window, method):
        return os.path.join(g_dir, '%s-%s-%s%s-hccs-%s.graphml' % (corpus, behaviour, window, alpha, method))

    fsa_v_15m = make_g_path('15m', fsa_v)
    knn_15m = make_g_path('15m', knn)
    t_15m = make_g_path('15m', threshold)

    fsa_v_60m = make_g_path('60m', fsa_v)
    knn_60m = make_g_path('60m', knn)
    t_60m = make_g_path('60m', threshold)

    fsa_v_360m = make_g_path('360m', fsa_v)
    knn_360m = make_g_path('360m', knn)
    t_360m = make_g_path('360m', threshold)

    fsa_v_1440m = make_g_path('1440m', fsa_v)
    knn_1440m = make_g_path('1440m', knn)
    t_1440m = make_g_path('1440m', threshold)

    log('loading the 15m graphs')
    fsa_v_15m_g = nx.read_graphml(fsa_v_15m)
    knn_15m_g = nx.read_graphml(knn_15m)
    t_15m_g = nx.read_graphml(t_15m)

    log('loading the 60m graphs')
    fsa_v_60m_g = nx.read_graphml(fsa_v_60m)
    knn_60m_g = nx.read_graphml(knn_60m)
    t_60m_g = nx.read_graphml(t_60m)

    log('loading the 360m graphs')
    fsa_v_360m_g = nx.read_graphml(fsa_v_360m)
    knn_360m_g = nx.read_graphml(knn_360m)
    t_360m_g = nx.read_graphml(t_360m)

    log('loading the 1440m graphs')
    fsa_v_1440m_g = nx.read_graphml(fsa_v_1440m)
    knn_1440m_g = nx.read_graphml(knn_1440m)
    t_1440m_g = nx.read_graphml(t_1440m)

    log('build fsa_v sim mtx')
    mtx_fsa_v = build_sim_mtx([fsa_v_15m_g, fsa_v_60m_g, fsa_v_360m_g, fsa_v_1440m_g], id_key, sim_measure)

    log('build knn sim mtx')
    mtx_knn = build_sim_mtx([knn_15m_g, knn_60m_g, knn_360m_g, knn_1440m_g], id_key, sim_measure)

    log('build threshold sim mtx')
    mtx_t = build_sim_mtx([t_15m_g, t_60m_g, t_360m_g, t_1440m_g], id_key, sim_measure)

    # log('build 60m sim mtx')
    # mtx_60m = build_sim_mtx([fsa_v_60m_g, knn_60m_g, t_60m_g], id_key, sim_measure)
    #
    # log('build 360m sim mtx')
    # mtx_360m = build_sim_mtx([fsa_v_360m_g, knn_360m_g, t_360m_g], id_key, sim_measure)
    #
    # log('build 1400m sim mtx')
    # mtx_1440m = build_sim_mtx([fsa_v_1440m_g, knn_1440m_g, t_1440m_g], id_key, sim_measure)

    mtxs = [mtx_fsa_v, mtx_knn, mtx_t]

    # global min/max used to share colourbar across all the matrices
    global_min = 0.0  # min(min([min(row) for row in m]) for m in mtxs)
    global_max = 1.0  # max(max([max(row) for row in m]) for m in mtxs)

    def plot(fig, ax, mtx, title, colourbar=False):
        img_opts = {
            'interpolation' : 'nearest', 'origin' : 'upper',
            'vmin' : global_min, 'vmax' : global_max
        }
        img = ax.imshow(mtx, **img_opts)

        # Fix FixedLocator warning: https://stackoverflow.com/a/63755285
        ax.xaxis.set_major_locator(mticker.MaxNLocator(4))
        xticks_loc = ax.get_xticks().tolist()
        ax.xaxis.set_major_locator(mticker.FixedLocator(xticks_loc))
        ax.yaxis.set_major_locator(mticker.MaxNLocator(4))
        yticks_loc = ax.get_yticks().tolist()
        ax.yaxis.set_major_locator(mticker.FixedLocator(yticks_loc))

        # getting the font sizes right took some time
        ax.set_title(title, fontsize=18)
        ax.set_xticklabels(['', '15', '60', '360', '1440', ''], fontsize=12)
        ax.set_yticklabels(['', '1440m', '360m', '60m', '15m', ''], fontsize=14)

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
                #cmap='viridis',  # deprecated as of matplotlib 3.3
                cax=cax
            )

    fig, (ax_fsa_v, ax_knn, ax_t) = plt.subplots(1, 3, figsize=(10, 2.5))
    plot(fig, ax_fsa_v, mtx_fsa_v, 'FSA_V')
    plot(fig, ax_knn, mtx_knn, 'kNN')
    plot(fig, ax_t, mtx_t, 'Threshold', colourbar=True)

    # plt.tight_layout()

    if opts.interactive:
        plt.show()

    if not opts.dry_run:
        plt.savefig(img_file, bbox_inches='tight', pad_inches=0)

    log('Done')
