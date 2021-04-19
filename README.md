# find_hccs

_Finding sets of accounts that appear to coordinate their behaviour in social media._

This project provides a pipeline of processing steps to uncover _highly coordinating communities_ (HCCs) within _latent coordination networks_ (LCNs) built through inferring connects between social media actors based on their behaviour. It also provides a number of supporting scripts and analysis tools for evaluating the pipeline's performance, plus datasets on which it has been tested for
the following publications:

- Weber, D. and Neumann, F. 2020. "Who's in the gang? Revealing coordinating communities on social media", _The 2020 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining_, _ASONAM 2020_, The Hague, Netherlands, 7-10 December, (accepted). ([arXiv:2010.08180](https://arxiv.org/abs/2010.08180))

- Weber, D. and Neumann, F. 2021, "A General Method to Find Highly Coordinating Communities in Social Media through Inferred Interaction Links", _Journal of Social Network Analysis and Mining_, submitted. ([arXiv:2103.03409](https://arxiv.org/abs/2103.03409))

- Weber, D. 2019. "On Coordinated Online Behaviour", Poster presented at _The Fourth Annual Australian Social Network Analysis Conference 2019_, _ASNAC 2019_, Adelaide, South Australia, 28-29 November. Available [here](https://www2.slideshare.net/derekweber/on-coordinated-online-behaviour).

- Weber, D., Nasim, M., Falzon, L. and Mitchell, L. 2020. "Revealing social bot communities through coordinated behaviour during the 2020 US Democratic and Republican National Conventions", Talk presented at _The Fifth Annual Australian Social Network Analysis Conference 2020_, _ASNAC 2020_, Perth, Western Australia, 26-27 November. Available [here](https://www.slideshare.net/derekweber/revealing-social-bot-communities-through-coordinated-behaviour).

- Weber, D., Nasim, M., Falzon, L. and Mitchell, L. 2020. "#ArsonEmergency and Australia’s “Black Summer”: A study of polarisation and its broader effect on the online discussion", Talk presented at _The Fifth Annual Australian Social Network Analysis Conference 2020_, _ASNAC 2020_, Perth, Western Australia, 26-27 November. Available [here](https://www.slideshare.net/derekweber/arsonemergency-and-australias-black-summer-a-study-of-polarisation-and-its-broader-effect-on-the-online-discussion).


## Dependencies

The code was developed using using Python 3.8.5 and Anaconda. Dependencies are listed in `environment.yml` (use first) with supplementary installations with `pip` (`requirements.txt`).

## The pipeline

The 10,000 foot view of the pipeline:

Infer links between social media accounts based on commonalities in their interactions (thus building a weighted graph of accounts, a _latent coordination network (LCN)_), and then extract highly connected communities, on the basis that those who are connected at anomalously high frequencies may be doing so deliberately.

To deal with large datasets (more than several hundred thousand tweets), we first extract relevant elements out to CSV files, and then process them to infer links between accounts (to build the LCN). Although this results in intermediate files, it provides a degree of flexibility. E.g., if I extract retweet information from a corpus of tweets with `raw_to_csv.py` (see below), then I can either infer links between accounts based on what individual tweets they both retweet **or** _who_ or _which account_ they both retweet.

The steps to the pipeline are as follows:

### 1. `raw_to_csv.py`

- **In**: Raw social media posts (e.g., tweets as JSON)
- **Out**: A CSV of interactions in the posts

Extract interaction data from raw social media posts (e.g., tweets) as CSV rows. Future versions may use JSON instead of CSV, because then column/key names are available with every data element, which can be handy when combining datasets of different interactions (e.g., hashtag uses with mentions). Additionally, they could be stored in a database rather than files.

`extract_in_conv_to_lcn.py` is used to link accounts when they join the same _conversation_, by which we mean that they both _reply_ into the same reply tree (rooted at the same original tweet). This script can output either a CSV of the reply interactions (and will need `find_behaviour.py` to infer the links) or an LCN of the inferred links, directly. `extract_in_conv.py` is deprecated, replaced by this script.

**NB** At some point, I intend to experiment shifting from CSV to JSON, so that the column names will be associated with each value in each record. This will increase the intermediate file size (but these could be compressed), but even if they're twice the size, they'll still be much smaller than the original tweets. Ultimately, using a database would be best.


### 2. `find_behaviour.py` and `find_behaviour_via_windows.py`

- **In**: A CSV of interactions
- **Out**: One/Many LCN(s) of accounts, linked through inference

Process the interactions, inferring links between accounts based on commonalities in the interaction metadata, and build an LCN from these links. The weight on links between accounts in the LCN corresponds to the _weight of evidence_ linking the two accounts, which may not be directly connected. An example is that an inferred link is created between two accounts when they retweet the same tweet. It could be coincidental, of course, but if it occurs unusually frequently, it may be an indicator of questionable activity.

The second script, `find_behaviour_via_windows.py` is used to segment the interactions into discrete time windows, and then an LCN is produced for each window.

The script `apply_decaying_sliding_window.py` can be used to produce a new _stream_ of LCNs by combining the LCN of the current window with those of the previous windows, with reduced weight based on a decaying parameter. The aim of this is to emphasise consistent coordination across multiple adjacent windows.

### 3. `combine_lcns.py`

- **In**: A directory of LCNs
- **Out**: A single combined LCN

The LCNs produced by `find_behaviour_via_windows.py` are then combined into a single LCN before extracting HCCs.

An alternative approach is to extract HCCs from each LCN before combining the HCCs. This would enable study of the growth and evolution of HCCs over time, but may struggle to find HCCs in windows with little activity.

### 4. `extract_hccs.py`

- **In**: An LCN, a weighted undirected graph of accounts
- **Out**: A graph of HCCs (each component is its own community)

Using one of the specified strategies and appropriate parameters, extract HCCs from the LCN. The strategies available are:

- FSA\_V: variant on [FSA](https://link.springer.com/article/10.1007/s13278-016-0319-z) specified in the paper
- kNN:  k Nearest Neighbour with k = ln(|U|)
- Threshold: keep only the x heaviest edges

## The data

The data used in the paper was collected, stored, analysed and reported on in accordance with ethics protocol **H-2018-045**, approved by the University of Adelaide's Human Research and Ethics Committee.

Data used includes:

- The 2016 tweets from [Twitter's 2018 Internet
Research Agency data dump](https://about.twitter.com/enus/values/elections-integrity.html). This is a dataset of approximately 1.5m tweets.
- A dataset based on a regional Australian election in March 2018. The election dataset was created using [RAPID](https://link.springer.com/chapter/10.1007/978-3-030-10997-4_44) and by filtering [Twitter's Standard `statuses/filter` API](https://developer.twitter.com/en/docs/tweets/filter-realtime/overview) with the screen names of 134 political candidate and party accounts
plus nine relevant hashtags. The collected tweets were augmented with all the tweets by the political accounts in the studied period, and all reply and quote chains within the period were also retrieved and added. This produced a dataset of approximately 115k tweets. The subset of tweets by the political accounts were treated as ground truth.

The IDs of the tweets in the election dataset are provided in the `data` folder, with the ground truth subset listed separately. These must be re-'hydrated' using a tool such as [Twarc](https://github.com/DocNow/twarc). Full tweet data cannot be uploaded, as per Twitter's terms and conditions.

## The analyses

A number of analyses and visualisations were prepared as part of the writing of the paper. These include:

- `interrogate_hccs.py`: Inspects the HCCs with the context of the LCN they came from, the tweets they posted and, optionally, [Botomoeter](https://botometer.iuni.iu.edu/#!/) bot rating information, and produces a rich JSON structure of information regarding the each HCC and its members' behaviour within the corpus.
- `run_hccs_reports.py`: Produces a number reports as CSV based on the interrogation results.
- `basic_network_stats.py`: Provides simple network information from a graphml file, which can contribute to spreadsheet tables.
- `build_features_cf_vis.py`: Creates a cumulative frequency chart from entropy values calculated from the frequency distributions of various features (e.g., hashtags, mentions, retweeted accounts) of the HCCs.
- `build_hashtag_co-mention_graph.py`: Creates a weighted graph of hashtags, linked when they are used in the same tweet or simply mentioned by the same account, based on a corpus of tweets. This can be used to identify topics of conversation and how they relate (whether they are connected at all, for example). We recommend visualisation with [visone](https://visone.info) or [Gephi](https://gephi.org/).
- `build_hccs_docsim_vis.py`: Creates a matrix visualisation, where each axis corresponds to a tweet or an account, and cell at coordinates (x,y) holds the similarity value (0 to 1) when comparing tweet x with tweet y or user x's tweets with user y's tweets. Similarity is calculated using cosine similarity on vectors in a doc-term matrix. The documents are either individual tweets or all the tweets of a user, while the terms are the words in the tweet (punctuation removed) or n-grams.
- `build_hccs_timeline_vis.py`: Creates a plot of HCC activity over time. If `merging` is applied, then `DBA.py` (dynamic barycentre averaging) is used to temporally average the HCCs timelines together.
- `compare_alpha_by_window_vis.py`: Used to examine the effect of using the decayed sliding window and variations in the decay factor.
- `compare_hcc_methods_by_window_vis.py`: Used to examine the overlap in the HCCs found with the different community detection methods.
- `compare_window_by_hcc_method_vis.py`: Used to examine the overlap in the HCCs found with the different window sizes, keeping the community detection method fixed.
- `DBA.py`: The [dynamic barycentre averaging](https://github.com/fpetitjean/DBA) used by `build_hccs_timeline_vis.py`.
- `expand_with_reasons.py`: Fleshes out an HCC by creating new nodes from the _reasons_ recorded for connecting the HCC nodes - i.e., if they retweeted the same tweet, a _reason_ would be the ID of the tweet they both retweeted. By examining this larger graph, it is possible to see which HCCs are related, through which _reason_ nodes connect them.
- `nodes_in_common.py`: Provided with two or more graphml files, determines what overlap there is in the graphs' nodes (based on a provided attribute, e.g. "label"), and prints out the result as a table ready for inclusion into a LaTeX paper.
- `top_hashtags_barchart_vis.py`: Produces a horizontal bar chart of the most used hashtags by the most active HCCs.
- `build_adr_vis.py`: Produces a scatter plot of account diversity ratio values (|accounts|/|tweets|) for each HCC in provided analyses (produced by `interrogate_hccs.py`)
- `build_itd_vis.py`: Produces a scatter plot of inter-arrivel time distributions for all HCCs in an analysis file (JSON). Each column is an HCC's posting timeline.

To build and use the machine learning classifier components, the following scripts are required, once HCCs have been detected:
- `hcc_graphml_to_csv.py`: extracts the HCC groups into a simple CSV with two columns, so each row consists of a community ID unique within the GraphML file and the account ID of a node within the HCC.
- `extract_feature_vectors_for_hcc_classifier(-ira).py`: using the HCC groupings, it builds the activity networks surrounding each HCC (i.e., the activity its members engage in, within the corpus) and then creates a feature vector for each member based on their profile details and also the details of the HCC (so each member's feature vector includes details of its HCC, which are duplicated amongst all the HCC's members).
- `train_hcc_classifier`: using positive feature vectors and non-positive feature vectors it trains a machine learning model to distinguish between the two using the SVM, RandomForest or Bagging Positive Unlabelled (BaggingPU) algorithm.
- `test_hcc_classifier`: applies the trained classifier against the feature vectors extracted for other discovered HCCs. Includes writing out ROC and AUC charts, if required.

## Supporting files and scripts

- `create_random_groups.py`: Used to create a random dataset for comparison with the HCCs. Using the remainder of accounts in a corpus, it assigns them randomly to groups matching the size distribution of the HCCs discovered in the corpus (but not including any of the HCC members).
- `cut_csv.py`: Convenience tool to manipulate CSV files - lets you cut out particular columns and output them in a new order.
- `decorate_network.py`: Adds attributes to the nodes of a GraphML file based on information from their tweet corpus and other sources.
- `filter_ira_csv_by_time.py`: Filters the Twitter IRA dataset CSV based on provided start and end timestamps.
- `filter_tweets_by_author.py`: Returns the tweets in a corpus posted by particular accounts. The order of filtered posts matches that in the corpus.
- `filter_csv.py`: Filters rows of a CSV file with a provided list of keywords, either ensuring they're included or excluded, as required.
- `filter_graph_by_edge_weight.py`: Filters a GraphML graph with weighted edges, keeping edges between the provided minimum and maximum values.
- `ira_stats.py`: Provides some simple statistics of a given IRA-formatted corpus.
- `net_log_utils.py`: Utility functions that relate to network matters (separated to avoid dependencies, allowing some scripts to run within a cygwin environment).
- `sort_csv_by_timestamp.py`: Sorts the rows in an IRA-formatted CSV by a timestamp in the 'timestamp' column.
- `utils.py`: Utility functions used by the scripts.

The `support` folder holds a number of scripts used for running the pipeline elements with a variety of parameters including window size, theta (for FSA\_V) and threshold parameters.

<!-- ## Example run-through -->
