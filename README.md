# find_hccs

_Finding sets of accounts that appear to coordinate their behaviour in social media._

This project provides a pipeline of processing steps to uncover _highly coordinating communities_ (HCCs)
within _latent coordination networks_ (LCNs) built through inferring connects between social media
actors based on their behaviour. It also provides a number of supporting scripts and analysis
tools for evaluating the pipeline's performance, plus datasets on which it has been tested for
the following publication:

Weber, D. & Neumann, F., "Who's in the gang? Revealing coordinating communities on social media",
_The 2020 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining_, _ASONAM 2020_, The Hague, Netherlands, 7-10 December, (submitted).

## The pipeline

The 10,000 foot view of the pipeline:

Infer links between social media accounts based on commonalities in their interactions
(thus building a weighted graph of accounts), and then extract highly connected
communities, on the basis that those who are connected at anomalously high
frequencies may be doing so deliberately.

The steps to the pipeline are as follows:

### 1. `raw_to_csv.py`

- **In**: Raw social media posts (e.g., tweets as JSON)
- **Out**: A CSV of interactions in the posts

Extract interaction data from raw social media posts (e.g., tweets) as CSV rows.
Future versions may use JSON instead of CSV, because then column/key names are
available with every data element, which can be handy when combining datasets of
different interactions (e.g., hashtag uses with mentions). Additionally, they
could be stored in a database rather than files.

### 2. `find_behaviour.py` and `find_behaviour_via_windows.py`

- **In**: A CSV of interactions
- **Out**: One/Many LCN(s) of accounts, linked through inference

Process the interactions, inferring links between accounts based on commonalities
in the interaction metadata, and build an LCN from these links. The weight on
links between accounts in the LCN corresponds to the _weight of evidence_ linking
the two accounts, which may not be directly connected. An example is that an
inferred link is created between two accounts when they retweet the same tweet.
It could be coincidental, of course, but if it occurs unusually frequently, it
may be an indicator of questionable activity.

The second script, `find_behaviour_via_windows.py` is used to segment the
interactions into discrete time windows, and then an LCN is produced for each
window.

The script `apply_decaying_sliding_window.py` can be used to produce a new
_stream_ of LCNs by combining the LCN of the current window with those of the
previous windows, with reduced weight based on a decaying parameter. The aim of
this is to emphasise consistent coordination across multiple adjacent windows.

### 3. `combine_lcns.py`

- **In**: A directory of LCNs
- **Out**: A single combined LCN

The LCNs produced by `find_behaviour_via_windows.py` are then combined into a
single LCN before extracting HCCs.

An alternative approach is to extract HCCs from each LCN before combining the
HCCs. This would enable study of the growth and evolution of HCCs over time, but
may struggle to find HCCs in windows with little activity.

### 4. `extract_hccs.py`

- **In**: An LCN, a weighted undirected graph of accounts
- **Out**: A graph of HCCs (each component is its own community)

Using one of the specified strategies and appropriate parameters, extract HCCs
from the LCN. The strategies available are:

- FSA_V: variant on [FSA](https://link.springer.com/article/10.1007/s13278-016-0319-z) specified in the paper
- kNN:  k Nearest Neighbour with k = ln(|U|)
- Threshold: keep only the x heaviest edges

## The data

The data used in the paper was collected, stored, analysed and reported on in
accordance with ethics protocol H-2018-045, approved by the University of
Adelaide's Human Research and Ethics Committee.

Data used includes:

- The 2016 tweets from [Twitter's 2018 Internet
Research Agency data dump](https://about.twitter.com/enus/values/elections-integrity.html). This is a dataset of approximately 1.5m tweets.
- A dataset based on a regional Australian election in March 2018. The election dataset was created using [RAPID](https://link.springer.com/chapter/10.1007/978-3-030-10997-4_44) and by filtering [Twitter's Standard `statuses/filter` API](https://developer.twitter.com/en/docs/tweets/filter-realtime/overview) with the screen names of 134 political candidate and party accounts
plus nine relevant hashtags. The collected tweets were augmented with all the tweets by the political accounts in the studied period, and all reply and quote chains within the period were also retrieved and added. This produced a dataset of approximately 115k tweets.

## The analyses

## Example run-through

## Supporting files and scripts
