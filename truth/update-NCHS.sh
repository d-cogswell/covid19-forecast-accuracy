#!/bin/bash
mkdir -p NCHS
wget https://data.cdc.gov/api/views/r8kw-7aab/rows.csv?accessType=DOWNLOAD -O NCHS/Provisional_COVID-19_Death_Counts_by_Week_Ending_Date_and_State.csv
