import os.path as osp
from os import walk
import pandas as pd
from datetime import datetime
from datetime import timedelta

import utils

dir = 'forecasts/covid19-forecast-hub/data-processed'


def list_models():
    _, dirnames, _ = next(walk(osp.join(dir)))
    dirnames.sort(key=str.lower)
    return(dirnames)


def print_stats(model='COVIDhub-ensemble'):
    forecast_dates = list_dates(model=model)

    if len(forecast_dates):
        earliest_forecast = forecast_dates[0]
        latest_forecast = forecast_dates[-1]

        days = 0
        for date in forecast_dates:
            forecast_df = load(date, model=model)
            if len(forecast_df['date']):
                last_day = forecast_df['date'].iat[-1]
                days = days + (last_day - date).days

        avg_forecast_len = days/len(forecast_dates)

        print(model)
        print("\tEarliest forecast: " + earliest_forecast.strftime('%Y-%m-%d'))
        print("\tLatest forecast: " + latest_forecast.strftime('%Y-%m-%d'))
        print("\tNumber of forecasts: " + str(len(forecast_dates)))
        print('\tAverage forecast length:', avg_forecast_len)


# Returns a dictionary of models and weights to create the ensemble
def ensemble_model_weights_cumDeaths(date, location="US"):
    datestr = pd.to_datetime(date).strftime('%Y-%m-%d')
    file = osp.join(dir, '../ensemble-metadata/',
                    datestr+'-cum_death-model-weights.csv')
    weights = pd.read_csv(file)

    # Filter for location and remove field
    loc = weights[weights['locations'] == location]
    loc = loc.drop('locations', 1)

    models = loc.keys()
    wts = loc[models].iloc[0]
    return(dict(zip(models, wts)))


def list_dates(model="COVIDhub-ensemble"):
    dates = []
    _, _, filenames = next(walk(osp.join(dir, model)))

    for f in filenames:
        # Get the date from the first 10 characters of the filename
        if model+".csv" in f:
            dates.append(pd.to_datetime(f[:10]))

    dates.sort()
    return(dates)


def load(date, location="US", model="COVIDhub-ensemble"):

    # Load locations table
    location_id = location
    loc_df = pd.read_csv(osp.join(dir, '../data-locations/locations.csv'))
    abbr = loc_df[loc_df['abbreviation'] == location]
    if len(abbr):
        location_id = abbr['location'].iat[0]
    else:
        location_id = loc_df[loc_df['location_name']
                             == location]['location'].iat[0]

    # Load the data file
    file = pd.to_datetime(date).strftime('%Y-%m-%d') + '-' + model + '.csv'
    data = pd.read_csv(osp.join(dir, model, file),
                       dtype={
        'location': str,  # Some locations are numbers, so set a dtype
    })

    # Filter for location
    data = data[data['location'] == location_id]

    # Filter for point data
    data = data[data['type'] == 'point']

    # Convert dates to datetime and sort
    data['target_end_date'] = pd.to_datetime(data['target_end_date'])
    data.sort_values('target_end_date', inplace=True)

    # #Define standard fields
    hospitalAdmissions_df = data[data['target'].str.contains('inc hosp')]
    deaths_df = data[data['target'].str.contains('inc death')]
    cumDeaths_df = data[data['target'].str.contains('cum death')]

    # Before 12/7/20, COVIDhub-ensemble hospitalizations are reported in a separate file downloaded from the CDC website
    if date < datetime(2020, 12, 7):
        hospitalAdmissions_df = load_CDC_ensemble_hospitalization(
            date, location=location)
    else:
        hospitalAdmissions_df = pd.DataFrame({
            'date': hospitalAdmissions_df['target_end_date'],
            'hospitalAdmissions': hospitalAdmissions_df['value']})

    # Create merged data frame
    merged_df = pd.merge(
        pd.DataFrame({'date': deaths_df['target_end_date'],
                      'deaths': deaths_df['value']}),
        pd.DataFrame({'date': cumDeaths_df['target_end_date'],
                      'cumDeaths': cumDeaths_df['value']}),
        on='date',
        how='outer')
    merged_df = pd.merge(merged_df, hospitalAdmissions_df,
                         how='outer', on='date', sort=True)
    return(merged_df)


# This function loads hospitalization forecasts downloaded from the CDC website
def load_CDC_ensemble_hospitalization(date, location="US", model="COVIDhub-ensemble"):
    dir = 'forecasts/CDC-ensemble-hospitalizations'

    # Get the file name
    file = ''
    dateStr = pd.to_datetime(date).strftime('%Y-%m-%d')
    _, _, filenames = next(walk(osp.join(dir)))
    for f in filenames:
        if 'hospitalizations-model-data' in f:
            if dateStr in f:
                file = f

    # Return an empty dataframe if file not found
    # The 6/1/2020 data is missing the 'target_end_date' field
    if file == '' or date == datetime(2020, 6, 1):
        return(
            pd.DataFrame({'date': pd.Series([], dtype='datetime64[ns]'),
                          'hospitalAdmissions': pd.Series([], dtype='float')}))

    data = pd.read_csv(osp.join(dir, file))

    # Filter for model
    if model != 'COVIDhub-ensemble':
        data = data[data['model'] == model]

    # Filter for location
    if location == 'US':
        location = 'National'
    # If location is an abbreviation, convert to name
    if location in utils.abbr_to_state.keys():
        location = utils.abbr_to_state[location]
    data = data[data['location_name'] == location]

    # Convert dates to datetime
    data['target_end_date'] = pd.to_datetime(data['target_end_date'])

    # Compute the ensemble average if necessary
    if model == 'COVIDhub-ensemble':
        if 'Ensemble' in data['model'].unique():
            data = data[data['model'] == 'Ensemble']
        else:
            # Calculate forcast for each model by summing all locations
            COVIDhub_df = pd.DataFrame()
            for m in data['model'].unique():

                # Sum over all locations and append
                model_df = data[data['model'] == m].groupby(
                    'target_end_date', as_index=False).sum()
                COVIDhub_df = COVIDhub_df.append(model_df)

            # Calculate the median of all models
            data = COVIDhub_df.groupby(
                'target_end_date', as_index=False).median()

    # Filter days ahead <= 28
    mask = data['target_end_date'] - date <= timedelta(days=28)

    # Define standard fields
    new_df = pd.DataFrame({
        'date': data['target_end_date'][mask],
        'hospitalAdmissions': data['point'][mask]
    })
    return(new_df)
