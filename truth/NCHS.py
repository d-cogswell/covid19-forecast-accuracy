import numpy as np
import pandas as pd

import utils


def load(location="US"):

    df = pd.read_csv(
        'truth/NCHS/Provisional_COVID-19_Death_Counts_by_Week_Ending_Date_and_State.csv')

    # If location is an abbreviation, convert to name
    if location in utils.abbr_to_state.keys():
        location = utils.abbr_to_state[location]

    if location == "US":
        location = "United States"

    # Filter for location
    df = df[df['State'] == location]

    # Filter for week
    df = df[df['Group'] == 'By Week']

    # Define standard fields
    df['date'] = pd.to_datetime(df['End Date'])
    df['deaths'] = df['COVID-19 Deaths'].fillna(0)/7
    df['cumDeaths'] = np.cumsum(df['COVID-19 Deaths'].fillna(0))

    return(df)
