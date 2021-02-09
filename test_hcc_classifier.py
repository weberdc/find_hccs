#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import sklearn
import statistics
import sys

# # import sklearn.external.joblib as joblib
# import joblib
# sys.modules['sklearn.externals.joblib'] = joblib

from argparse import ArgumentParser
from bagging_pu import BaggingClassifierPU
from joblib import load
from pandas.api.types import CategoricalDtype
from sklearn import svm, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from utils import eprint


class Options:
    def __init__(self):
        self.usage = 'test_hcc_classifier.py -c <classifier.joblib> -e <expected_positive_data.csv> -n <negative_training_data.csv> - ...'
        self._init_parser()


    def _init_parser(self):
        self.parser = ArgumentParser(usage=self.usage,conflict_handler='resolve')
        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            default=False,
            dest='verbose',
            help='Turn on verbose logging (default: False)'
        )
        self.parser.add_argument(
            '--upsample',
            action='store_true',
            default=False,
            dest='upsample',
            help='Turn on upsampling (default: False)'
        )
        self.parser.add_argument(
            '--standardise',
            action='store_true',
            default=False,
            dest='standardise',
            help='Standardise the data (default: False)'
        )
        self.parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            dest='dry_run',
            help='Do not save charts to disk (default: False)'
        )
        self.parser.add_argument(
            '-i', '--interactive-mode',
            action='store_true',
            default=False,
            dest='interactive_mode',
            help='Render performance plot to screen as well as file (default: False)'
        )
        self.parser.add_argument(
            '-c', '--classifier-file',
            required=True,
            dest='classifier_file',
            help='The file containing the persisted classification model.'
        )
        self.parser.add_argument(
            '-n', '--negative-data',
            required=True,
            dest='neg_test_file',
            help='The file of negative test data (class 0).'
        )
        self.parser.add_argument(
            '-e', '--exp-pos-data',
            required=True,
            dest='exp_pos_file',
            help='The file of real data to test (expected to be positive, class 1).'
        )
        self.parser.add_argument(
            '-o1', '--output1',
            required=True,
            dest='out_file1',
            help='The file to which to write the prediction histogram.'
        )
        self.parser.add_argument(
            '-o2', '--output2',
            required=True,
            dest='out_file2',
            help='The file to which to write the ROC curve plot.'
        )
        self.parser.add_argument(
            '--roc-label',
            default='',
            dest='roc_label',
            help='The label to include in the title of the ROC curve plot.'
        )

    def parse(self, args=None):
        return self.parser.parse_args(args)


def load_training_data(csv_file, first=False):
    # categories = CategoricalDtype(['COORDINATED','RANDOMISED'], ordered=True)
    return pd.read_csv(csv_file, comment='#')  #dtype={'Label':categories}, comment='#')


def plot_probabilities(series1, series2, interactive_mode, outfile):
    plt.clf()
    # plt.rcParams['font.size'] = 10
    # plt.rcParams['figure.figsize'] = 8, 4
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.hist(series1, color='red', edgecolor='black', bins=20, alpha=0.5)
    plt.hist(series2, color='blue', edgecolor='black', bins=20, alpha=0.5)
    plt.title('Probability of coordination')
    plt.xlabel('Degree of probability')
    plt.ylabel('Samples')
    plt.legend(['Coordination expected', 'No coordination expected'])
    if interactive_mode:
        plt.show()
        print('Wrote probability histogram to %s' % outfile)
    if not DRY_RUN:
        plt.savefig(outfile)


def plot_ROC_curve(label, model, expected_labels, test_data, interactive_mode, outfile):
    from sklearn.metrics import roc_curve
    from sklearn.metrics import roc_auc_score

    plt.clf()

    fig, ax = plt.subplots()

    # predict probabilities
    probs = model.predict_proba(test_data)
    # keep probabilities for the positive outcome only
    probs = probs[:, 1]
    # calculate AUC
    auc = roc_auc_score(expected_labels, probs)
    print('AUC: %.3f' % auc)
    # calculate roc curve
    fpr, tpr, thresholds = roc_curve(expected_labels, probs)
    ax.set(title='ROC curve for coordination (%s)' % label, xlabel='Specificity', ylabel='Sensitivity')
    textstr = 'AUC: %.3f' % auc

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='square', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    if auc > 0.5:
        ax.text(0.75, 0.25, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)
    else:
        ax.text(0.15, 0.75, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)

    # plot no skill
    ax.plot([0, 1], [0, 1], linestyle='--')
    # plot the roc curve for the model
    ax.plot(fpr, tpr, marker='.')
    if not DRY_RUN:
        plt.savefig(outfile)
        print('Wrote ROC curve to %s' % outfile)
    # show the plot
    if interactive_mode:
        plt.show()



DEBUG=False
def log(msg):
    if DEBUG: eprint(msg)

DRY_RUN=False

COORDINATED = 1
RANDOMISED = 0


if __name__ == '__main__':

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose
    DRY_RUN=opts.dry_run

    neg_test_file    = opts.neg_test_file
    exp_pos_file     = opts.exp_pos_file
    cls_file         = opts.classifier_file
    out_file1        = opts.out_file1
    out_file2        = opts.out_file2
    interactive_mode = opts.interactive_mode
    roc_label        = opts.roc_label
    upsample         = opts.upsample
    standardise      = opts.standardise

    # COORDINATED = 1, RANDOMISED = 0
    oth_data = load_training_data(neg_test_file)
    oth_data.drop('Label', axis=1, inplace=True)
    exp_pos_data = load_training_data(exp_pos_file)
    exp_pos_data.drop('Label', axis=1, inplace=True)

    if standardise:
        from sklearn.preprocessing import StandardScaler
        combined = pd.concat([exp_pos_data, oth_data])
        scaler = StandardScaler().fit(combined)
        standardised = pd.DataFrame(scaler.transform(combined), columns=exp_pos_data.columns)
        exp_pos_data = standardised.iloc[:len(exp_pos_data), :]
        oth_data = standardised.iloc[len(exp_pos_data):, :]

    oth_labels = pd.DataFrame([RANDOMISED] * len(oth_data), columns=['Label'])  #oth_data['Label']
    exp_pos_labels = pd.DataFrame([COORDINATED] * exp_pos_data.shape[0], columns=['Label'])

    print('Unlabeled data:         %s' % str(oth_data.shape))
    print('Expected positive data: %s' % str(exp_pos_data.shape))

    classifier = load(cls_file)

    # Create a balanced real test dataset:
    # balance expected positive with negative data
    sampler = max if upsample else min
    sample_size = sampler(len(exp_pos_data), len(oth_data))

    print('Sample size: %d' % sample_size)
    real_test_data   = pd.concat([exp_pos_data.sample(sample_size, replace=True), oth_data.sample(sample_size, replace=True)])
    real_test_labels = pd.concat([exp_pos_labels.sample(sample_size, replace=True), oth_labels.sample(sample_size, replace=True)], sort=False)

    predictions = classifier.predict(real_test_data)

    print('real test data   %s' % str(real_test_data.shape))
    print('real test labels %s' % str(real_test_labels.shape))

    print("Classification report for classifier %s:\n%s\n" % (
        classifier, metrics.classification_report(real_test_labels, predictions)
    ))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(real_test_labels, predictions))

    def print_stats_header():
        print('Label\tMin\t1st Q.\t2nd Q.\t3rd Q.\tMax\tMean')
    def print_stats(lbl, l):
        stats = [np.min(l),np.percentile(l, 25),np.median(l),np.percentile(l,75),np.max(l),np.mean(l)]
        print('%s\t%s' % (lbl, '\t'.join(map(lambda f: '%.3f' % f, stats))))

    predicted_probabilities = classifier.predict_proba(real_test_data)
    print_stats_header()
    print_stats('Neg. ', classifier.predict_proba(oth_data)[:,1])  # want low
    print_stats('Coord', predicted_probabilities[:,1])                # average

    plot_probabilities(
        predicted_probabilities[:,1][:len(exp_pos_data)],
        predicted_probabilities[:,1][len(exp_pos_data):],
        interactive_mode,
        out_file1
    )

    plot_ROC_curve(roc_label, classifier, real_test_labels, real_test_data, interactive_mode, out_file2)
