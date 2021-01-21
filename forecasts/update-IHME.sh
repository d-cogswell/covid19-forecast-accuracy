#!/bin/bash

#Screen scrape the list of data files
files=`curl -s http://www.healthdata.org/covid/data-downloads | egrep -o '\https?://ihmecovid19storage.blob.core.windows.net/archive/[^ ]+.zip'`

#Download and extract new data sets
for f in $files
do
  echo $f
  date=`echo $f | sed 's/.*archive\/\(.*\)\/ihme-covid19.zip/\1/'`

  #If folder doesn't exist, download data
  if [ ! -d "IHME/$date" ]
  then
    echo "Downloading $f"
    wget -P IHME/$date $f
  fi
  
  #Extract the summary stats, the file name has changed over time so try them all
  for csv_file in [ "ihme-covid19_all_locs.csv" "hospitalization_all_locs_corrected.csv" "Hospitalization_all_locs.csv" "reference_hospitalization_all_locs.csv" "Reference_hospitalization_all_locs.csv" ]
  do
    unzip -j -n IHME/$date/ihme-covid19.zip */$csv_file -d IHME/$date/
  done
done