#!/bin/bash
git_dir=covid19-forecast-hub

#Clone the repo if doesn't exist, otherwise pull
if [ ! -d $git_dir ]
then
    git clone https://github.com/reichlab/covid19-forecast-hub.git
else
    git -C $git_dir pull
fi