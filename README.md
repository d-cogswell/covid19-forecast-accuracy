# Compare COVID19 forcasts against truth data

A collection of Bash and Python scripts to download, process, plot, and compare COVID19 data and forecasts.

## Truth data sources

- JHU CSSE: https://coronavirus.jhu.edu/
- covidtracking.com: https://covidtracking.com/

### Not yet implemented

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
