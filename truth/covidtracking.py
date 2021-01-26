import pandas as pd


def load(location="US"):

    # US and state date are in different files
    if location == "US":
        df = pd.read_csv('truth/covidtracking.com/national-history.csv')
    else:
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
