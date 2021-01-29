#!/bin/bash
mkdir -p healthdata.gov
wget https://healthdata.gov/node/3565481/download -O healthdata.gov/reported_hospitalization_utilization_timeseries.csv
