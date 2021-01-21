#!/bin/bash
mkdir -p CSSE

URL="https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
wget $URL -O CSSE/time_series_covid19_confirmed_US.csv

URL="https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
wget $URL -O CSSE/time_series_covid19_deaths_US.csv
