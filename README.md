# Compare COVID19 forcasts against truth data

A collection of Bash and Python scripts to download, process, plot, and compare COVID19 data and forecasts. Each separate data set has its own unique organziation, and the goal of this project is to provide a standard way of manipulating data from different sources. Each data set is loaded as a Pandas dataframe with the following standardized fields:
- `date` : calendar date for each record, stored as a `datetime` object
- `cases` : new number cases reported each day
- `cumCases` : the cumulative number of cases that have been reported
- `hosptialAdmissions` : new hospital admissions reported each day
- `hospitalizedCurrently` : number of people currently hospitalized at each date
- `deaths` : new number of deaths reported each day
- `cumDeaths` : the cumulative number of deaths

## Truth data sources

- JHU CSSE: https://coronavirus.jhu.edu/
- covidtracking.com: https://covidtracking.com/
- healthdata.gov: https://healthdata.gov/dataset/covid-19-reported-patient-impact-and-hospital-capacity-state-timeseries

## Forecasts available:

- CDC ensemble forecasts: https://www.cdc.gov/coronavirus/2019-ncov/covid-data/mathematical-modeling.html
- IHME: https://covid19.­healthdata.org

## Installation

Data can be downloaded by running the following commands from the root directory. Beware that the forecasting data requires >20GB of storage space, and the initial download takes significant time. Running the commands again will fetch and process any new data.

Download/update forecast data:
```bash
  ./update-forecasts.sh
```

Download/udpate truth data:
```bash
  ./update-truth.sh
```
