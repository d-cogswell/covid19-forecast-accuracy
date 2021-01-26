import numpy as np
import pandas as pd

import utils


def load(location="US"):

    def process_csv(file, location):
        df = pd.read_csv(file)

        # Group by location and sum deaths
        if location == "US":
            df = df.groupby('Country_Region').sum()
        else:

            # If location is an abbreviation, convert to name
            if location in utils.abbr_to_state.keys():
                location = utils.abbr_to_state[location]

            df = df[df['Province_State'] == location]
            df = df.groupby('Province_State').sum()

        return(df)

    # Load cases
    df_confirmed = process_csv(
        'truth/CSSE/time_series_covid19_confirmed_US.csv', location)
    dates = df_confirmed.keys().array[5:]  # Dates begin in th 5th column
    cumCases = df_confirmed[dates].iloc[0]
    cases = np.diff(cumCases, prepend=0)

    # Load deaths
    df_deaths = process_csv(
        'truth/CSSE/time_series_covid19_deaths_US.csv', location)
    dates = df_deaths.keys().array[6:]  # Dates begin in the 6th column
    cumDeaths = df_deaths[dates].iloc[0]
    deaths = np.diff(cumDeaths, prepend=0)

    # Build a new dataframe with date as a key
    new_df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'cases': cases,
        'cumCases': cumCases,
        'deaths': deaths,
        'cumDeaths': cumDeaths})
    return(new_df)
