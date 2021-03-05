import numpy as np
import pandas as pd
from datetime import datetime

import utils


def load(location="US"):

    df = pd.read_csv(
        'truth/healthdata.gov/reported_hospitalization_utilization_timeseries.csv')

    if location == "US":
        # Group by date to combine state data
        df = df.groupby('date', as_index=False).sum()

    else:

        # If location is an name, convert to abbreviation
        if location in utils.state_to_abbr.keys():
            location = utils.state_to_abbr[location]

        df = df[df['state'] == location]

    # Covert date field to datetime and sort
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['date'], inplace=True)

    # Do not load data before July 15, 2020
    df = df[df['date'] >= datetime(2020, 7, 15)]

    # See notes here for hospital admissions:
    # https://github.com/reichlab/covid19-forecast-hub/tree/master/data-processed
    # Values checked against https://ourworldindata.org/covid-hospitalizations
    hospitalAdmissions = df['previous_day_admission_adult_covid_confirmed'] + \
        df['previous_day_admission_pediatric_covid_confirmed']
    hospitalAdmissions = hospitalAdmissions.array
    hospitalAdmissions = np.append(hospitalAdmissions[1:], 0)

    # Define standard fields
    df['hospitalAdmissions'] = hospitalAdmissions
    df['hospitalizedCurrently'] = df['total_adult_patients_hospitalized_confirmed_covid'] + \
        df['total_pediatric_patients_hospitalized_confirmed_covid']

    # Remove last entry due to hospital admissions date shift
    return(df[:-1])
