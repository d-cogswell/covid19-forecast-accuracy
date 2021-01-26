import pandas as pd

import utils


def load(location="US"):

    # US and state date are in different files
    if location == "US":
        df = pd.read_csv('truth/covidtracking.com/national-history.csv')
    else:

        # If location is an name, convert to abbreviation
        if location in utils.state_to_abbr.keys():
            location = utils.state_to_abbr[location]

        df = pd.read_csv('truth/covidtracking.com/all-states-history.csv')
        df = df[df['state'] == location]

    # Covert date field to datetime and sort
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['date'], inplace=True)

    # Define standard fields
    df['cases'] = df['positiveIncrease']
    df['cumCases'] = df['positive']
    df['deaths'] = df['deathIncrease']
    df['cumDeaths'] = df['death']

    return(df)
