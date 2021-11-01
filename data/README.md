# Data

The `data` folder holds files with the IDs of tweets collected as part of a number of studies. To make use of these IDs, the tweets will need to be 'hydrated' from the IDs (e.g., using a tool like [Twarc](https://github.com/DocNow/twarc#hydrate))

## Dataset Descriptions

**2018 March**

The filter terms used included nine hashtags (`#abetterway`, `#ausunions`, `#realchange`, `#saelection`, `#saparli`, `#sapol`, `#savotes`, `#savotes2018`, `#liberals`) and the screen names of 134 political candidate and party accounts (and are withheld to comply with ethics protocol H-2018-045 approved by the University of Adelaide's human research and ethics committee, but can be provided on request).

- `ds1_tweet-ids.txt.gz`: Dataset 1
- `gt_tweet-ids.txt.gz`: Ground Truth

<!--
Dataset 1 and Ground Truth were used in the following publications:

- Weber, D. and Neumann, F., "Who's in the Gang? Revealing Coordinating Communities in Social Media.", In _The 2020 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining_, _ASONAM_, Leiden, The Netherlands, 7-10 December, 2020, accepted. (arXiv: https://arxiv.org/abs/2010.08180)

- Weber, D. and Neumann, F. 2021, "A General Method to Find Highly Coordinating Communities in Social Media through Inferred Interaction Links", _Journal of Social Network Analysis and Mining_, submitted. ([arXiv:2103.03409](https://arxiv.org/abs/2103.03409))
-->

**ArsonEmergency**: This dataset was used to examine polarisation and misinformation during Australia's Black Summer bushfires (2019-2020) and all data was collected with Twarc.

- `ArsonEmergency-20191231-20200117-tweet_ids.txt.gz`: Twitter activity including 'ArsonEmergency' 2019-12-31 to 2020-01-17

**US 2020 Democratic and Republican Conventions (DNC, RNC)**:

- `USPol-dnc-20200817-20200821-tweet_ids.txt.gz`: Tweets collected over 2020 DNC, specifically 2020-08-17 to 2020-08-21
- `USPol-rnc-20200824-20200828-tweet_ids.txt.gz`: Tweets collected over 2020 RNC, specifically 2020-08-24 to 2020-08-28

These datasets were used in the following publications:

- Weber, D., Nasim, M., Falzon, L. and Mitchell, L. (2020) "#ArsonEmergency and Australia's 'Black
Summer': Polarisation and misinformation on social media". Lecture Notes in Computer
Science pp 159–173, DOI 10.1007/978-3-030-61841-4 11, ([arXiv:2004.00742](https://arxiv.org/abs/2004.00742))

- Weber, D. and Neumann, F., "Who's in the Gang? Revealing Coordinating Communities in Social Media.", In _The 2020 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining_, _ASONAM_, Leiden, The Netherlands, 7-10 December, 2020, https://doi.org/10.1109/asonam49781.2020.9381418. (arXiv: https://arxiv.org/abs/2010.08180)

- Weber, D., Neumann, F. 2021, "Amplifying influence through coordinated behaviour in social networks", _Journal of Social Network Analysis and Mining_, 11(1), 111. https://doi.org/10.1007/s13278-021-00815-2 ([arXiv:2103.03409](https://arxiv.org/abs/2103.03409))


**Persistent Echo Chambers**

This study examined the activites and content of two pairs of polarised groups (the ArsonEmergency groups and a second pair active during Australia's marriage equality postal survey in 2017) over a longitudinal setting, through three Twitter datasets covering different discussion topics.

- `ArsonEmergency-20191231-20200117-tweet_ids.txt.gz`: Twitter activity including the keyword 'ArsonEmergency' 2019-12-31 to 2020-01-17
- `ssm-original-tweet_ids.txt.gz`: Twitter activity collected from September to November 2017 relating to the Australian marriage equality (same-sex marriage, SSM) postal survey using the keywords '\#MarriageEquality', '\#SSM', '\#auspol', '\#VoteYes', and '\#VoteNo', in which the users of \#VoteYes and \#VoteNo were found to be clearly polarised.
- `ssm-election-tweet_ids.txt.gz`: The activities of the \#VoteYes and \#VoteNo accounts in the three weeks leading up to and just past the Australian federal election in May 2019.
- `afl-rapid-20190322_25-tweet_ids.txt.gz`: A 72 hour collection of discussion surrounding the Australian Football League (AFL) sports competition (keyword: 'afl').

These datasets were used in the following publications:

- Mehwish Nasim, Derek Weber, Tobin South, Jonathan Tuke, Nigel Bean, Lucia Falzon and Lewis Mitchell (in preparation), "A longitudinal study of the echo chamber effect in the Australian Twittersphere".
