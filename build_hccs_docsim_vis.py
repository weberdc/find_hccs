#!/usr/bin/env python3

import json
import lda
import matplotlib.pyplot as plt
import nltk
import numpy as np
import re
import sys
import utils

# from scipy import sparse

from argparse import ArgumentParser
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import sparse
# from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity

# Builds a doc term matrix from the tweets posted by HCCs and then does cosine
# similarity between all tweets in the hope that tweets within HCCs are more
# similar to each other than to tweets outside.

class Options:
    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'build_hccs_docsim_vis.py -i <hcc_infos>.json -o <sim_mtx_vis>.pdf [-w|--word] [--lda <l>] [-n|--n-gram <n>]'

        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument(
            '-i',
            required=True,
            dest='hcc_infos_file',
            help='Info about HCCs extracted by interrogate_hccs.py'
        )
        self.parser.add_argument(
            '-o',
            required=True,
            dest='img_file',
            help='Visualisation of the cosine similarity matrix'
        )
        self.parser.add_argument(
            '--lda',
            default=0,
            type=int,
            dest='lda_clusters',
            help='Run LDA looking for this many topics'
        )
        self.parser.add_argument(
            '-n', '--n-gram',
            default=5,
            type=int,
            dest='n_gram_size',
            help='Size of n-grams (default: 5)'
        )
        self.parser.add_argument(
            '-t', '--title',
            default=None,
            dest='title',
            help='Title for the chart (default: HCCs info filename)'
        )
        self.parser.add_argument(
            '-iw', '--width',
            dest='img_width',
            type=float,
            default=4,
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
            '-fs', '--font-size',
            dest='label_font_size',
            type=float,
            default=14,
            help='The font size of the inner label (default: 14)'
        )
        self.parser.add_argument(
            '-lx', '--label-x',
            dest='label_x',
            type=float,
            default=0.04,
            help='The x coordinate of the inner label (default: 6)'
        )
        self.parser.add_argument(
            '-ly', '--label-y',
            dest='label_y',
            type=float,
            default=0.92,
            help='The y coordinate of the inner label (default: 6)'
        )
        self.parser.add_argument(
            '--ly-delta',
            dest='label_y_delta',
            type=float,
            default=-0.06,
            help='The delta to apply to the y coordinate of the inner label (default: 6)'
        )
        self.parser.add_argument(
            '-w', '--word',
            dest='use_words',
            action='store_true',
            default=False,
            help='Use words for n-grams, not characters (default: False)'
        )
        self.parser.add_argument(
            '-u', '--user',
            dest='use_users',
            action='store_true',
            default=False,
            help='Combine all tweets of each user to make larger documents (default: False)'
        )
        self.parser.add_argument(
            '--downsample',
            dest='downsample',
            action='store_true',
            default=False,
            help='Apply downsample to reduce the size of the rendered similarity matrix (default: False)'
        )
        self.parser.add_argument(
            '--no-title',
            dest='no_title',
            action='store_true',
            default=False,
            help='Do not include a title (default: False)'
        )
        self.parser.add_argument(
            '--tweets-in-label',
            dest='tweets_in_label',
            action='store_true',
            default=False,
            help='Include tweet count in the internal label (default: False)'
        )
        self.parser.add_argument(
            '--no-colour-bar', '--no-color-bar', '--no-colourbar', '--no-colorbar',
            dest='no_cb',
            action='store_true',
            default=False,
            help='Do not include a colour bar (default: False)'
        )
        self.parser.add_argument(
            '--normalise-lower-bound',
            dest='normalise_lb',
            action='store_true',
            default=False,
            help='Force colour bar to start from 0 (default: False)'
        )
        self.parser.add_argument(
            '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help='Dry run - do not write image files (default: False)'
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


def clean_text(full_text):
    t = re.sub('https://t.co/', '', full_text)
    t = re.sub('https?://', '', t)
    t = re.sub(r'[^A-Za-z0-9. @#]', '', t)
    t = re.sub('\s+', ' ', t)
    t = t.casefold()  # like .lower() but works on non-Western alphabets
    return t


DEBUG=False
def log(msg):
    if DEBUG: utils.eprint(msg)


if __name__=='__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    hcc_infos_file = opts.hcc_infos_file
    lda_clusters = opts.lda_clusters
    img_file = opts.img_file
    use_words = opts.use_words
    use_users = opts.use_users
    apply_downsample = opts.downsample
    n = opts.n_gram_size
    title = opts.title if opts.title else utils.extract_filename(hcc_infos_file)
    img_w = opts.img_width
    img_h = opts.img_height

    STARTING_TIME = utils.now_str()
    log('Starting at %s\n' % STARTING_TIME)

    hcc_infos = []
    with open(hcc_infos_file, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            hcc_infos.append(json.loads(line))

    hcc_infos.sort(key=lambda info: info['tweet_count'], reverse=True)

    # community_ids = [i['community_id'] for i in hcc_infos]
    log('Communities: %d' % len(hcc_infos))
    log('Populations: %s' % ','.join(list(map(lambda i: '%d' % i['user_count'], hcc_infos))))

    docs = {}
    ordered_doc_ids = []
    line_count = 0
    for hcc_info in hcc_infos:
        users = list(hcc_info['tweets_by_users'])
        # order users by those who tweet most first
        users.sort(key=lambda u: hcc_info['tweets_by_users'][u], reverse=True)
        for u in users:
            tweets = list(filter(lambda t: t['u_id'] == u, hcc_info['tweets']))
            tweets.sort(key=lambda t: t['t_ts'])
            if use_users:
                ordered_doc_ids.append(u)
            for t in tweets:
                line_count = utils.log_row_count(line_count, DEBUG)
                if not use_users:
                    ordered_doc_ids.append(t['t_id'])

                text = clean_text(t['text'])

                if use_words:
                    tokens = text.split()  # [''.join(fg) for fg in fivegrams]
                    # print(docs[t['t_id']])
                else:  # character n-grams
                    fivegrams = nltk.ngrams(text, n)
                    tokens = [''.join(fg) for fg in fivegrams]
                    # print(docs[t['t_id']])
                if use_users:
                    if u not in docs:
                        docs[u] = []
                    docs[u] += tokens
                else:
                    docs[t['t_id']] = tokens
                # if line_count >=5: sys.exit()

    # code borrowed from https://datascience.blog.wzb.eu/2016/06/17/creating-a-sparse-document-term-matrix-for-topic-modeling-via-lda/
    n_nonzero = 0
    vocab = set()
    for docterms in docs.values():
        unique_terms = set(docterms)    # all unique terms of this doc
        vocab |= unique_terms           # set union: add unique terms of this doc
        n_nonzero += len(unique_terms)  # add count of unique terms in this doc

    # make a list of document names
    # the order will be the same as in the dict
    docnames = ordered_doc_ids  # list(docs.keys())

    docnames = np.array(docnames)
    vocab = np.array(list(vocab))

    log('\nvocab.shape: %s' % str(vocab.shape))
    log('docnames.shape: %s' % str(docnames.shape))

    vocab_sorter = np.argsort(vocab)    # indices that sort "vocab"

    ndocs = len(docnames)
    nvocab = len(vocab)

    data = np.empty(n_nonzero, dtype=np.intc)     # all non-zero term frequencies at data[k]
    rows = np.empty(n_nonzero, dtype=np.intc)     # row index for kth data item (kth term freq.)
    cols = np.empty(n_nonzero, dtype=np.intc)     # column index for kth data item (kth term freq.)

    log('data.shape: %s' % str(data.shape))

    ind = 0     # current index in the sparse matrix data
    # go through all documents with their terms
    for docname, terms in docs.items():
        # find indices into  such that, if the corresponding elements in  were
        # inserted before the indices, the order of  would be preserved
        # -> array of indices of  in
        term_indices = vocab_sorter[np.searchsorted(vocab, terms, sorter=vocab_sorter)]

        # count the unique terms of the document and get their vocabulary indices
        uniq_indices, counts = np.unique(term_indices, return_counts=True)
        n_vals = len(uniq_indices)  # = number of unique terms
        ind_end = ind + n_vals  #  to  is the slice that we will fill with data

        data[ind:ind_end] = counts                  # save the counts (term frequencies)
        cols[ind:ind_end] = uniq_indices            # save the column index: index in
        doc_idx = np.where(docnames == docname)     # get the document index for the document name
        rows[ind:ind_end] = np.repeat(doc_idx, n_vals)  # save it as repeated value

        ind = ind_end  # resume with next document -> add data to the end

    dtm = sparse.coo_matrix((data, (rows, cols)), shape=(ndocs, nvocab), dtype=np.intc)


    if img_file:
        # cosine similarity: https://stackoverflow.com/a/39104306
        # similarities = cosine_similarity(dtm)
        # print('pairwise dense output:\n {}\n'.format(similarities))

        #also can output sparse matrices
        similarities_sparse = cosine_similarity(dtm, dense_output=False)
        # print('pairwise sparse output:\n {}\n'.format(similarities_sparse))

        # shannon's entropy?

        dim = similarities_sparse.shape[0]

        # downsample the sim_mtx: https://stackoverflow.com/a/42210862
        if apply_downsample:
            data = similarities_sparse
            N, M = data.shape
            s, t = dim//100, dim//100  #400, 400  # decimation factors for y and x directions
            T = sparse.csc_matrix((np.ones((M,)), np.arange(M), np.r_[np.arange(0, M, t), M]), (M, (M-1) // t + 1))
            S = sparse.csr_matrix((np.ones((N,)), np.arange(N), np.r_[np.arange(0, N, s), N]), ((N-1) // s + 1, N))
            downsample = S @ data @ T  # downsample by binning into s x t rectangles
        else:
            downsample = similarities_sparse
        downsample = downsample.todense() # ready for plotting

        # visualise it
        fig, ax = plt.subplots(figsize=(img_w, img_h))

        img_opts = {
            'interpolation' : 'nearest',
            'origin' : 'lower'
        }
        if opts.normalise_lb: img_opts['vmin'] = 0
        img = ax.imshow(downsample, **img_opts)
        x = opts.label_x  # 0.04
        y = opts.label_y  # 0.92
        text = 'Communities: %d' % len(hcc_infos)
        if opts.tweets_in_label:
            text += '\nTweets: %d' % line_count
            y -= opts.label_y_delta  # 0.06
        ax.text(
            x, y, text, fontsize=opts.label_font_size, transform=ax.transAxes,
            bbox={'boxstyle':'square', 'facecolor':'white'}
        )

        if not opts.no_title:
            ax.set_title(title)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        if opts.no_cb:
            # fix subplot sizing: https://stackoverflow.com/a/42397467
            cax.axis('off')
        else:
            fig.colorbar(
                img,
                ax=ax,
                cmap='viridis',
                cax=cax
            )

        # if not opts.no_cb:
        #     fig.colorbar(img, ax=ax, cmap='viridis')

        # img.set_clim(vmin=0)
        if not opts.dry_run:
            plt.savefig(img_file, bbox_inches = 'tight', pad_inches = 0)
        else:
            plt.show()



    if lda_clusters:
        model = lda.LDA(n_topics=lda_clusters, n_iter=1000, random_state=1)

        model.fit(dtm)

        topic_word = model.topic_word_
        n_top_words = 3

        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
            print('Topic {}: {}'.format(i, ' '.join(topic_words)))


    log('\nHaving started at %s,' % STARTING_TIME)
    log('now ending at     %s' % utils.now_str())
