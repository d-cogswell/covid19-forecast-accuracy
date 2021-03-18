#!/bin/bash
mkdir -p healthdata.gov
wget https://healthdata.gov/api/views/g62h-syeh/rows.csv?accessType=DOWNLOAD -O healthdata.gov/COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv
