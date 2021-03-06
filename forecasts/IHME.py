import os.path as osp
from os import walk
import pandas as pd

import utils

dir = 'forecasts/IHME/'

# The name of the data file changed at different points in time.
# This list contains different names that were used.
csv_files = [
    "ihme-covid19_all_locs.csv",
    "hospitalization_all_locs_corrected.csv",
    'Hospitalization_all_locs.csv',
    "reference_hospitalization_all_locs.csv",
    "Reference_hospitalization_all_locs.csv"
]


def list_dates(model=None):
    dates = []
    for (dirpath, dirnames, filenames) in walk(dir):
        for d in dirnames:
            dates.append(pd.to_datetime(d))
    dates.sort()
    return(dates)


def load(date, location="United States of America", model=None):
    location_dict = {
        "US": "United States of America",
    }

    if location in location_dict.keys():
        location = location_dict[location]

    # Find the data file by checking multiple file names
    csv_path = ''
    for f in csv_files:
        path = osp.join(dir, pd.to_datetime(date).strftime('%Y-%m-%d'), f)
        if osp.exists(path):
            csv_path = path
    data = pd.read_csv(csv_path, dtype={
        'confirmed_infections_data_type': str,
        'seroprev_data_type': str})

    # If location is an abbreviation, convert to name
    if location in utils.abbr_to_state.keys():
        location = utils.abbr_to_state[location]

    # If 'United States of America' doesn't exist in 'location_name', try 'US'
    # This was an issue in some of the early data sets
    if location == "United States of America" and data['location_name'].str.contains('US').any():
        location = 'US'

    # Filter for location
    data = data[data['location_name'] == location]

    # Create 'date' field if it doesn't exist
    if 'date' not in data.keys():
        data['date'] = data['date_reported']

    # Convert date field to datetime and sort
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by=['date'], inplace=True)

    # Filter for dates after prediction date
    data = data[data['date'] > date]

    # Define standard fields
    data['hospitalizedCurrently'] = data['allbed_mean']
    data['hospitalAdmissions'] = data['admis_mean']
    data['deaths'] = data['deaths_mean']
    data['cumDeaths'] = data['totdea_mean']

    return(data)
