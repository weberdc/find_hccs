#!/bin/sh

CSV1=$1
CSV2=$2
OCSV=$3

head -1 $CSV1 > /tmp/header.csv

tail -n+2 $CSV1 > /tmp/f1.csv
tail -n+2 $CSV2 > /tmp/f2.csv

cat /tmp/f1.csv /tmp/f2.csv | sort > /tmp/f.csv

cat /tmp/header.csv /tmp/f.csv > $OCSV

