#!/bin/bash
git_dir=covid19-forecast-hub

#Clone the repo if doesn't exist, otherwise pull
if [ ! -d $git_dir ]
then
    git clone https://github.com/reichlab/covid19-forecast-hub.git
else
    git -C $git_dir pull
fi


#Get additional hospitalization forecasts only available at the CDC website
storage_dir="CDC-ensemble-hospitalizations"
URL="https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/forecasting-hospitalizations-previous.html"
files=`curl -s $URL | egrep -o '\/[^ ]*(-all)?-hospitalizations-model-data.csv'`

#Download data files
for f in $files
do
  
  #Check if filename does not contain "national"
  if [[ ! "$f" == *"national"* ]]
  then
    
    #Download file if it doesn't exist yet
    fname=`echo $f | egrep -o '[0-9]{4}-[0-9]{2}-[0-9]{2}[^ ]*.csv'`
    if [ ! -f $storage_dir/$fname ]
    then
      echo "Downloading https://www.cdc.gov/$f"
      wget -P $storage_dir https://www.cdc.gov/$f
    fi
  fi
done