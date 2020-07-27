@echo off

rem produce all CSVs from raw

@echo Started: %date% %time% 1>&2

set DATASET=ira_tweets-2016.csv.gz
set OPTS=--ira

set RAW_TO_CSV=python %LCN_BIN%\raw_to_csv.py      -i %DATASET% %OPTS%
set EX_IN_CONV=python %LCN_BIN%\extract_in_conv.py -i %DATASET% %OPTS%

set CORPUS=ira

echo ALL_DOMAINS
%RAW_TO_CSV% -o %CORPUS%-all_domains.csv  --topic ALL_DOMAINS
echo ALL_HASHTAGS
%RAW_TO_CSV% -o %CORPUS%-all_hashtags.csv --topic ALL_HASHTAGS
echo ALL_MENTIONS
%RAW_TO_CSV% -o %CORPUS%-all_mentions.csv --topic ALL_MENTIONS
echo ALL_URLS
%RAW_TO_CSV% -o %CORPUS%-all_urls.csv     --topic ALL_URLS
echo DOMAINS
%RAW_TO_CSV% -o %CORPUS%-domains.csv      --topic DOMAINS
echo HASHTAGS
%RAW_TO_CSV% -o %CORPUS%-hashtags.csv     --topic HASHTAGS
echo MENTIONS
%RAW_TO_CSV% -o %CORPUS%-mentions.csv     --topic MENTIONS
echo RETWEETS
%RAW_TO_CSV% -o %CORPUS%-retweets.csv     --topic RETWEETS
echo URLS
%RAW_TO_CSV% -o %CORPUS%-urls.csv         --topic URLS
echo IN_CONV
%EX_IN_CONV% -o %CORPUS%-inconv.csv

@echo Ended:   %date% %time% 1>&2
