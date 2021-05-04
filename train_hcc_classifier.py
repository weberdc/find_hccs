#!/usr/bin/env python3

import csv
# import math
import matplotlib.pyplot as plt
# import networkx as nx
import numpy as np
import pandas as pd
import random
import sklearn
import statistics
import sys


from argparse import ArgumentParser
from bagging_pu import BaggingClassifierPU
from joblib import dump
from pandas.api.types import CategoricalDtype
from sklearn import svm, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier
# from summarise_numbers import quartile
from utils import eprint, tsver  #, fetch_lines


class Options:
    def __init__(self):
        self.usage = 'train_hcc_classifier.py -p <positive_training_data.csv> -n <negative_training_data.csv> -o <classifier.joblib> ...'
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
            '--skip-std',
            action='store_true',
            default=False,
            dest='skip_std',
            help='Skip standard classification and go straight to bagging PU (default: False)'
        )
        self.parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            dest='dry_run',
            help='Dry run - do not write models to disk (default: False)'
        )
        self.parser.add_argument(
            '-i', '--interactive-mode',
            action='store_true',
            default=False,
            dest='interactive_mode',
            help='Render performance plot to screen as well as file (default: False)'
        )
        self.parser.add_argument(
            '-p', '--positive-data',
            required=True,
            dest='pos_training_file',
            help='The file of positive training data.'
        )
        self.parser.add_argument(
            '-n', '--negative-data',
            required=True,
            dest='other_training_file',
            help='The file of unlabeled, non-positive training data.'
        )
        self.parser.add_argument(
            '-o', '--classifier-file',
            required=True,
            dest='classifier_file_prefix',
            help='The prefix for the classifier files to produce (as joblib).'
        )


    def parse(self, args=None):
        return self.parser.parse_args(args)


def load_training_data(csv_file, first=False):
    return pd.read_csv(csv_file, comment='#')


def classify_with_svc(pos_data, pos_labels, oth_data, oth_labels):
    classifier = svm.SVC(gamma=0.001, probability=True)

    pos_count = pos_data.shape[0]
    neg_count = oth_data.shape[0]

    training_data   = pd.concat([pos_data.iloc[::2], oth_data[:neg_count // 2]])
    training_labels = pd.concat([pos_labels.iloc[::2], oth_labels[:neg_count // 2]])
    test_data       = pd.concat([pos_data.iloc[1::2], oth_data[neg_count // 2:]])
    test_labels     = pd.concat([pos_labels.iloc[1::2], oth_labels[neg_count // 2:]])
    # training_data   = pd.concat([pos_data[:pos_count // 2], oth_data[:neg_count // 2]])
    # training_labels = pd.concat([pos_labels[:pos_count // 2], oth_labels[:neg_count // 2]])
    # test_data       = pd.concat([pos_data[pos_count // 2:], oth_data[neg_count // 2:]])
    # test_labels     = pd.concat([pos_labels[pos_count // 2:], oth_labels[neg_count // 2:]])

    print('test label shapes: %s' % str(test_labels.shape))

    # We learn the digits on the first half of the digits
    classifier.fit(training_data, training_labels)

    expected = test_labels  # pd.concat([pos_labels, oth_labels[neg_count // 2:]])
    predicted = classifier.predict(test_data)

    print("Classification report for classifier %s:\n%s\n" % (
        classifier, metrics.classification_report(expected, predicted)
    ))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

    return classifier


COORDINATING = 1
UNLABELED = 0


def calc_confusion_matrix(model, X, y, positive=COORDINATING, unlabeled=UNLABELED):
    test_data, labels = X, y
    tp, tn, fp, fn = np.zeros(4)

    predictions = model.predict(test_data)

    for i in range(labels.shape[0]):
        actual = labels.iloc[i]       # Series
        prediction = predictions[i]  # ndarray
        if actual == positive and prediction == positive:
            tp += 1
        if actual == positive and prediction == unlabeled:
            fn += 1
        if actual == unlabeled and prediction == positive:
            fp += 1
        if actual == unlabeled and prediction == unlabeled:
            tn += 1

    return dict(tp=tp, tn=tn, fp=fp, fn=fn)


def pos_recall(model, X, y):
    cm = calc_confusion_matrix(model, X, y)
    tp = cm['tp']
    fn = cm['fn']

    # props to https://en.wikipedia.org/wiki/Precision_and_recall
    return tp / (tp + fn)


def pos_precision(model, X, y):
    cm = calc_confusion_matrix(model, X, y)
    tp = cm['tp']
    fp = cm['fp']

    # props to https://en.wikipedia.org/wiki/Precision_and_recall
    return tp / (tp + fp)


def pos_precision(model, X, y):
    cm = calc_confusion_matrix(model, X, y)
    tp = cm['tp']
    fp = cm['fp']

    # props to https://en.wikipedia.org/wiki/Precision_and_recall
    return tp / (tp + fp)


def class_f1(model, X, y, label=COORDINATING):
    test_data, labels = X, y

    return metrics.precision_recall_fscore_support(
        labels, model.predict(test_data), pos_label=label, average='binary'
    )[2]  # returns [precision, recall, fbeta_score, support]


def pos_f1(model, X, y):
    return class_f1(model, X, y, COORDINATING)


def unl_f1(model, X, y):
    return class_f1(model, X, y, UNLABELED)


def classify_with_svc3(pos_data, pos_labels, oth_data, oth_labels):
    # classifier = svm.SVC(C=1, random_state=0)#(gamma=0.001, probability=True)
    classifier = svm.SVC(gamma=0.001, probability=True)
    classify_with(classifier, pos_data, pos_labels, oth_data, oth_labels)
    return classifier

def classify_with_rfc2(pos_data, pos_labels, oth_data, oth_labels):
    classifier = RandomForestClassifier(
        n_estimators = 1000,  # Use 1000 trees
        n_jobs = -1           # Use all CPU cores
    )
    classify_with(classifier, pos_data, pos_labels, oth_data, oth_labels)
    return classifier

def classify_with_bagging_pu2(pos_data, pos_labels, oth_data, oth_labels, hidden_size, seed=None):
    classifier = BaggingClassifierPU(
        DecisionTreeClassifier(),
        random_state = seed,  # random number generator seed
        n_estimators = 1000,  # 1000 trees as usual
        # max_samples = oth_labels.shape[0],# sum(y), # Balance the positives and unlabeled in each bag
        n_jobs = -1           # Use all cores
    )
    classify_with(classifier, pos_data, pos_labels, oth_data, oth_labels)
    return (classifier, None)


def classify_with(classifier, pos_data, pos_labels, oth_data, oth_labels):

    data   = pos_data.append(oth_data, ignore_index=True)
    labels = pos_labels.append(oth_labels, ignore_index=True)['Label']

    scoring = {
        'f1': 'f1',
        'precision': 'precision',
        'recall': 'recall',
        'accuracy': 'accuracy',
        'precision_macro': 'precision_macro',
        'recall_macro': 'recall_macro',
        'pos_recall': pos_recall,
        'pos_precision': pos_precision,
        'pos_f1': pos_f1,
        'unl_f1': unl_f1,
    }

    scores = cross_validate(classifier, data, labels, cv=10, scoring=scoring)

    print(f'Accuracy: {scores["test_accuracy"].mean():.2f}')
    print(f'f_{{1p}}: {scores["test_pos_f1"].mean():.2f}')
    print(f'f_{{1u}}: {scores["test_unl_f1"].mean():.2f}')
    print(f'P_prec:   {scores["test_pos_precision"].mean():.2f}')
    print(f'P_recall: {scores["test_pos_recall"].mean():.2f}')

    classifier.fit(data, labels)  # now train on everything

    expected  = labels
    predicted = classifier.predict(data)

    print("Classification report for classifier %s:\n%s\n" % (
        classifier, metrics.classification_report(expected, predicted)
    ))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

    return classifier


# def classify_with_svc2(pos_data, pos_labels, oth_data, oth_labels):
#     classifier = svm.SVC(gamma=0.001, probability=True)
#
#     def train_classifier(cls, pos_data, pos_labels, oth_data, oth_labels):
#
#         pos_count = pos_data.shape[0]
#         neg_count = oth_data.shape[0]
#
#         print('pre-loop pos_data: %s' % str(pos_data.shape))
#         print('pre-loop oth_data: %s' % str(oth_data.shape))
#
#         for i in range(pos_count):
#             print('i: %d' % i)
#             test_pos_data   = pos_data.iloc[i]
#             test_pos_labels = pos_labels.iloc[i]
#             print('test_pos_data:   %s' % str(test_pos_data.shape))
#             print('test_pos_labels: %s' % str(test_pos_labels.shape))
#             if i == 0:
#                 train_pos_data   = pos_data.iloc[1:]
#                 train_pos_labels = pos_labels.iloc[1:]
#             elif i == pos_count - 1:
#                 train_pos_data   = pos_data.iloc[:-1]
#                 train_pos_labels = pos_labels.iloc[:-1]
#             else:
#                 train_pos_data   = pd.concat([pos_data.iloc[:i],   pos_data.iloc[i+1:]])
#                 train_pos_labels = pd.concat([pos_labels.iloc[:i], pos_labels.iloc[i+1:]])
#             print('train_pos_data:   %s' % str(train_pos_data.shape))
#             print('train_pos_labels: %s' % str(train_pos_labels.shape))
#             train_pos_data   = train_pos_data.sample(neg_count // 2, replace=True)
#             train_pos_labels = train_pos_labels.sample(neg_count // 2, replace=True)
#             training_data   = pd.concat([train_pos_data,   oth_data[:neg_count // 2]])
#             training_labels = pd.concat([train_pos_labels, oth_labels[:neg_count // 2]])
#             # test_data       = oth_data[neg_count // 2:].append(test_pos_data, ignore_index=True)  # pd.concat([test_pos_data,    oth_data[neg_count // 2:]])
#             # test_labels     = oth_labels[neg_count // 2:].append(test_pos_labels, ignore_index=True)  # pd.concat([test_pos_labels,  oth_labels[neg_count // 2:]])
#
#             test_data       = oth_data[neg_count // 2:]
#             test_labels     = oth_labels[neg_count // 2:]
#             for j in range(10):
#                 test_data = test_data.append(test_pos_data, ignore_index=True)  # pd.concat([test_pos_data,    oth_data[neg_count // 2:]])
#                 test_labels = test_labels.append(test_pos_labels, ignore_index=True)  # pd.concat([test_pos_labels,  oth_labels[neg_count // 2:]])
#
#             # training_data   = pd.concat([pos_data[:pos_count // 2], oth_data[:neg_count // 2]])
#             # training_labels = pd.concat([pos_labels[:pos_count // 2], oth_labels[:neg_count // 2]])
#             # test_data       = pd.concat([pos_data[pos_count // 2:], oth_data[neg_count // 2:]])
#             # test_labels     = pd.concat([pos_labels[pos_count // 2:], oth_labels[neg_count // 2:]])
#
#             print('test data shape:  %s' % str(test_data.shape))
#             print('test label shape: %s' % str(test_labels.shape))
#             print('train data shape:  %s' % str(training_data.shape))
#             print('train label shape: %s' % str(training_labels.shape))
#
#             # We learn the digits on the first half of the digits
#             classifier.fit(training_data, training_labels)
#
#             expected = test_labels  # pd.concat([pos_labels, oth_labels[neg_count // 2:]])
#             predicted = classifier.predict(test_data)
#
#             print("Classification report for classifier %s:\n%s\n" % (
#                 classifier, metrics.classification_report(expected, predicted)
#             ))
#             # print('F1-score:%s' % metrics.f1_score(expected, predicted.ravel()))
#             print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
#
#     train_classifier(classifier, pos_data, pos_labels, oth_data, oth_labels)
#
#     return classifier



def classify_with_rfc(pos_data, pos_labels, oth_data, oth_labels):
    classifier = RandomForestClassifier(
        n_estimators = 1000,  # Use 1000 trees
        n_jobs = -1           # Use all CPU cores
    )
    pos_count = pos_data.shape[0]
    neg_count = oth_data.shape[0]

    training_data   = pd.concat([pos_data.iloc[::2], oth_data[:neg_count // 2]])
    training_labels = pd.concat([pos_labels.iloc[::2], oth_labels[:neg_count // 2]])
    test_data       = pd.concat([pos_data.iloc[1::2], oth_data[neg_count // 2:]])
    test_labels     = pd.concat([pos_labels.iloc[1::2], oth_labels[neg_count // 2:]])

    print('test label shapes: %s' % str(test_labels.shape))

    # We learn the digits on the first half of the digits
    classifier.fit(training_data, training_labels)

    expected = test_labels  # pd.concat([pos_labels, oth_labels[neg_count // 2:]])
    predicted = classifier.predict(test_data)

    print("Classification report for classifier %s:\n%s\n" % (
        classifier, metrics.classification_report(expected, predicted)
    ))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

    return classifier


def classify_with_bagging_pu(pos_data, pos_labels, oth_data, oth_labels, hidden_size, seed=None):

    # inspired by https://roywright.me/2017/11/16/positive-unlabeled-learning/
    X = pd.concat([pos_data, oth_data], sort=False)
    y = pd.concat([pos_labels, oth_labels], ignore_index=True)
    y = pd.Series([l for l in y['Label']])
    print(y.shape)
    # y = y.astype(int)  # convert 'COORDINATED' to 1 and 'RANDOMISED' to 0

    # Check the contents of the set
    print('%d data points and %d features' % (X.shape))
    print('%d positive out of %d total' % (sum(y), len(y)))

    # Keep the original targets safe for later
    y_orig = y.copy()

    # Unlabel a certain number of data points
    y.loc[
        np.random.choice(
            y[y == 1].index,
            replace = False,
            size = hidden_size
        )
    ] = 0

    # Check the new contents of the set
    print('%d positive out of %d total' % (sum(y), len(y)))

    # We'll use a generic random forest
    rf = RandomForestClassifier(
        random_state = seed,  # random number generator seed
        n_estimators = 1000,  # Use 1000 trees
        n_jobs = -1           # Use all CPU cores
    )
    rf.fit(X, y)

    # We'll also add an SVC
    svc = svm.SVC(
        random_state = seed,  # random number generator seed
        probability=True,     # so we can call predict_proba
        kernel='poly',        # kernels include: rbf, sigmoid, linear, poly
        gamma='scale'         # also 0.001
    )  # gamma=0.001,
    svc.fit(X, y)
    # results['output_svc'] = svc.predict_proba(X)[:,1]

    # Store the scores assigned by this approach
    results = pd.DataFrame({
        'truth'      : y_orig,   # The true labels
        'label'      : y,        # The labels to be shown to models in experiment
        'output_std' : rf.predict_proba(X)[:,1],   # The random forest's scores
        'output_svc' : svc.predict_proba(X)[:,1]
    }, columns = ['truth', 'label', 'output_std', 'output_svc'])

    bc = BaggingClassifierPU(
        DecisionTreeClassifier(),
        random_state = seed,  # random number generator seed
        n_estimators = 1000,  # 1000 trees as usual
        max_samples = sum(y), # Balance the positives and unlabeled in each bag
        n_jobs = -1           # Use all cores
    )
    bc.fit(X, y)
    results['output_skb'] = bc.oob_decision_function_[:,1]

    expected = y_orig #test_labels  # pd.concat([pos_labels, oth_labels[neg_count // 2:]])
    predicted = results['output_skb']  # probabilities - classifier.predict(test_data)
    # print(predicted)
    predicted_labels = [(1 if p >= 0.5 else 0) for p in predicted]

    print("Classification report for classifier %s:\n%s\n" % (
        bc, metrics.classification_report(expected, predicted_labels)
    ))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted_labels))


    return (bc, results)


def plot_bagging_pu_results(results, hidden_size, interactive_mode, filepath):
    # For each data point, calculate the average score from the three approaches
    results['output_all'] = results[[
        'output_std', 'output_svc', 'output_skb'
    ]].mean(axis = 1)

    # Prepare for graphing the performance
    # (i.e. the success in identifying hidden positives)
    ts = range(1, hidden_size, 1)  # (100, hidden_size, 100)
    y_std, y_svc, y_skb, y_all = [], [], [], []
    for t in ts:
        y_std.append(
            results[results.label == 0].sort_values(
                'output_std', ascending = False
            ).head(t).truth.mean()
        )
        y_svc.append(
            results[results.label == 0].sort_values(
                'output_svc', ascending = False
            ).head(t).truth.mean()
        )
        y_skb.append(
            results[results.label == 0].sort_values(
                'output_skb', ascending = False
            ).head(t).truth.mean()
        )
        y_all.append(
            results[results.label == 0].sort_values(
                'output_all', ascending = False
            ).head(t).truth.mean()
        )

    # Performance graphing
    plt.clf()
    plt.rcParams['font.size'] = 16
    plt.rcParams['figure.figsize'] = 15, 8

    # print('y_std: %s' % y_std)
    # print('y_svc: %s' % y_svc)
    # print('y_skb: %s' % y_skb)
    # print('y_all: %s' % y_all)

    plt.plot(
        ts, y_std,
        ts, y_svc,
        ts, y_skb,
        ts, y_all,
        lw = 3
    )

    vals = plt.gca().get_yticks()
    plt.yticks(vals, ['%.0f%%' % (v*100) for v in vals])
    plt.xlabel('Number of unlabeled data points chosen from the top rated')
    plt.ylabel('Percent of chosen that are secretly positive')
    plt.legend([
        'Standard classifier',
        'Scalable Vector Machine',
        'PU bagging',
        'Average score'
    ])
    ylim = plt.gca().get_ylim()
    plt.title('Performance of the two approaches and of their average')
    plt.grid()
    plt.savefig(filepath)
    if interactive_mode:
        plt.show()


def plot_pca(pos_data, pos_labels, oth_data, oth_labels):
    def plot_2d_space(X, y, label='Classes'):
        plt.clf()
        colors = ['#1F77B4', '#FF7F0E']
        markers = ['o', 's']
        for l, c, m in zip(np.unique(y), colors, markers):
            plt.scatter(
                X[y==l, 0],
                X[y==l, 1],
                c=c, label=l, marker=m
            )
        plt.title(label)
        plt.legend(loc='upper right')
        plt.show()

    from sklearn.decomposition import PCA

    X = pd.concat([pos_data, oth_data], axis=0, ignore_index=True)
    y = pd.concat([pos_labels, oth_labels])['Label']

    # https://stackoverflow.com/a/26415620
    # from sklearn import preprocessing
    #
    # x = X.values #returns a numpy array
    # min_max_scaler = preprocessing.MinMaxScaler()
    # x_scaled = min_max_scaler.fit_transform(x)
    # X = pd.DataFrame(x_scaled)

    pca = PCA(n_components=2)
    X = pca.fit_transform(X)

    plot_2d_space(X, y, 'Imbalanced dataset (2 PCA components)')


# def plot_probabilities(series1, series2, interactive_mode):
#     plt.clf()
#     # plt.rcParams['font.size'] = 10
#     # plt.rcParams['figure.figsize'] = 8, 4
#     plt.rcParams['font.family'] = 'Times New Roman'
#     plt.hist(series1, color='red', edgecolor='black', bins=20)
#     plt.hist(series2, color='blue', edgecolor='black', bins=20)
#     plt.title('Probability of coordination')
#     plt.xlabel('Degree of probability')
#     plt.ylabel('Samples')
#     plt.legend(['Coordination expected', 'No coordination expected'])
#     if interactive_mode:
#         plt.show()


DEBUG=False
def log(msg):
    if DEBUG: eprint(msg)


COORDINATED = 1
RANDOMISED = 0


if __name__ == '__main__':

    print('START:', tsver())

    options = Options()
    opts = options.parse(sys.argv[1:])

    DEBUG=opts.verbose

    file_prefix = opts.classifier_file_prefix
    skip_std    = opts.skip_std
    dry_run     = opts.dry_run
    int_mode    = opts.interactive_mode
    upsample    = opts.upsample
    standardise = opts.standardise

    VER = tsver()

    print('Training classifiers with key: %s' % VER)

    def mkfn(classifier):
        return '%s-%s-%s.joblib' % (file_prefix, classifier, VER)

    print('COORDINATED = 1, RANDOMISED = 0')
    pos_data = load_training_data(opts.pos_training_file, True)
    pos_data.drop('Label', axis=1, inplace=True)
    oth_data = load_training_data(opts.other_training_file)
    oth_data.drop('Label', axis=1, inplace=True)

    original_pos_data_length = len(pos_data)
    original_oth_data_length = len(oth_data)

    sampler = max if upsample else min
    sample_size = sampler(original_pos_data_length, original_oth_data_length)
    print('Sample size: %d' % sample_size)

    tmp = pos_data.sample(sample_size, replace=True)
    pos_data = tmp

    if standardise:
        from sklearn.preprocessing import StandardScaler
        combined = pd.concat([pos_data, oth_data])
        scaler = StandardScaler().fit(combined)
        standardised = pd.DataFrame(scaler.transform(combined), columns=pos_data.columns)
        pos_data = standardised.iloc[:len(pos_data), :]
        oth_data = standardised.iloc[len(pos_data):, :]

    pos_labels = pd.DataFrame([COORDINATED] * len(pos_data), columns=['Label'])  # pos_data['Label']
    oth_labels = pd.DataFrame([RANDOMISED] * len(oth_data), columns=['Label'])  #oth_data['Label']

    print('Positive data:    %s' % str(pos_data.shape))
    print('Unlabeled data:   %s' % str(oth_data.shape))
    print('Positive labels:  %s' % str(pos_labels.shape))
    print('Unlabeled labels: %s' % str(oth_labels.shape))

    # print(oth_data.head(30))

    if int_mode:
        plot_pca(pos_data, pos_labels, oth_data, oth_labels)
        plot_pca(
            pos_data.sample(original_oth_data_length, replace=True),
            pos_labels.sample(original_oth_data_length, replace=True),
            oth_data, oth_labels
        )
        # sys.exit()

    svc = classify_with_svc3(pos_data, pos_labels, oth_data, oth_labels)
    svc_file = mkfn('svc')
    if not dry_run:
        dump(svc, svc_file)
        print('Wrote SVM classifier to %s' % svc_file)

    # svc2  = classify_with_svc2(pos_data, pos_labels, oth_data, oth_labels)
    # svc2_file = mkfn('svc2')
    # if not dry_run:
    #     dump(svc2, svc2_file)
    #     print('Wrote SVM classifier to %s' % svc2_file)

    rfc = classify_with_rfc2(pos_data, pos_labels, oth_data, oth_labels)
    rfc_file = mkfn('rfc')
    if not dry_run:
        dump(rfc, rfc_file)
        print('Wrote RandomForest classifier to %s' % rfc_file)

    hidden_size = int(len(pos_data) * 0.5)

    (bc, results) = classify_with_bagging_pu2(pos_data, pos_labels, oth_data, oth_labels, hidden_size, seed=1)
    # (bc, results) = classify_with_bagging_pu(pos_data.sample(len(oth_data), replace=True), pos_labels.sample(len(oth_data), replace=True), oth_data, oth_labels, hidden_size, seed=1)

    if results:
        bpu_comparison_chart_fn = '%s-bpu-comparison-%s.png' % (file_prefix, VER)
        plot_bagging_pu_results(results, hidden_size, int_mode, bpu_comparison_chart_fn)

    bc_file = mkfn('bpu')
    if not dry_run:
        dump(bc, bc_file)
        print('Wrote classifier to %s' % bc_file)

    print('DONE:', tsver())
