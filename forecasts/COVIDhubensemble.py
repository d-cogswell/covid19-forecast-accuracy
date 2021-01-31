import os.path as osp
from os import walk
import pandas as pd

dir = 'forecasts/covid19-forecast-hub/data-processed'


def list_models():
    _, dirnames, _ = next(walk(osp.join(dir)))
    return(dirnames)


def list_dates(model="COVIDhub-ensemble"):
    dates = []
    _, _, filenames = next(walk(osp.join(dir, model)))

    for f in filenames:
        # Get the date from the first 10 characters of the filename
        if "csv" in f:
            dates.append(pd.to_datetime(f[:10]))

    dates.sort()
    return(dates)


def load(date, location="US", model="COVIDhub-ensemble"):

    # Load locations table
    loc_df = pd.read_csv(osp.join(dir, '../data-locations/locations.csv'))
    abbr = loc_df[loc_df['abbreviation'] == location]
    if len(abbr):
        location = abbr['location'].iat[0]
    else:
        location = loc_df[loc_df['location_name']
                          == location]['location'].iat[0]

    # Load the data file
    file = pd.to_datetime(date).strftime('%Y-%m-%d') + '-' + model + '.csv'
    data = pd.read_csv(osp.join(dir, model, file),
                       dtype={
        'location': str,  # Some locations are numbers, so set a dtype
    })

    # Filter for location
    data = data[data['location'] == location]

    # Filter for point data
    data = data[data['type'] == 'point']

    # Convert dates to datetime and sort
    data['target_end_date'] = pd.to_datetime(data['target_end_date'])
    data.sort_values('target_end_date', inplace=True)

    # #Define standard fields
    hospitalAdmissions_df = data[data['target'].str.contains('inc hosp')]
    hospitalAdmissions_df = pd.DataFrame({
        'date': hospitalAdmissions_df['target_end_date'],
        'hospitalAdmissions': hospitalAdmissions_df['value']})

    cumDeath_df = data[data['target'].str.contains('cum death')]
    cumDeath_df = pd.DataFrame({
        'date': cumDeath_df['target_end_date'],
        'cumDeaths': cumDeath_df['value']})

    # Create merged data frame
    merged = pd.merge(hospitalAdmissions_df, cumDeath_df,
                      on='date', sort=True, how='outer')
    return(merged)
