#!/bin/bash
mkdir -p covidtracking.com
wget https://covidtracking.com/data/download/national-history.csv -O covidtracking.com/national-history.csv
wget https://covidtracking.com/data/download/all-states-history.csv -O covidtracking.com/all-states-history.csv
