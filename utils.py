import numpy as np
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime


def moving_avg(x, N):
    return(np.convolve(x, np.ones((N,))/N, mode='valid'))


def xaxis_months(fig, ax):
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    fig.autofmt_xdate()


def get_location_string(location):
    if location in abbr_to_state.keys():
        return(abbr_to_state[location])
    else:
        return(location)


holidays = {
    'Easter': datetime(2020, 4, 12),
    'Memorial Day': datetime(2020, 5, 25),
    'Independence Day': datetime(2020, 7, 4),
    'Labor Day': datetime(2020, 9, 7),
    'Thanksgiving': datetime(2020, 11, 26),
    'Christmas': datetime(2020, 12, 25),
    'New years': datetime(2021, 1, 1),
    'Texas storms': datetime(2021, 2, 13)
}


state_to_abbr = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

abbr_to_state = dict(map(reversed, state_to_abbr.items()))


# Error functions, F is forecast, A is actual
def abs_err(F, A):
    return(np.abs(F-A))


def rel_err(F, A):
    return((F-A)/A)


def abs_rel_err(F, A):
    return(np.abs((F-A)/A))


# Returns an array of errors for each deate in model_dates, evaulated using errorFunc
def model_error(true_dates, true_vals, model_dates, model_vals, errorFunc):
    true_dict = dict(zip(true_dates, true_vals))
    model_dict = dict(zip(model_dates, model_vals))

    error = []
    for date in model_dict.keys():
        # Make sure the true value exists
        try:
            if true_dict[date]:
                error.append(errorFunc(model_dict[date], true_dict[date]))
        except Exception:
            error.append(None)
            pass

    return(error)


def compute_error_all_forecasts(forecast, truth_df, errorFunc,
                                field='cumDeaths', dates=None,
                                location="US", model="COVIDhub-ensemble"):
    """Returns a DataFrame with error computed for every forecast"""
    df = pd.DataFrame({'forecast_date': [], 'date': [],
                       'days_ahead': [], 'error': []})
    if dates is None:
        dates = forecast.list_dates(model)

    for d in dates:
        data = forecast.load(d, location=location, model=model)

        # Compute the error
        err = model_error(truth_df['date'], truth_df[field],
                          data['date'], data[field], errorFunc)
        time_diff = data['date']-d
        days = time_diff.dt.days.tolist()

        new = pd.DataFrame({'forecast_date': [
                           d]*len(err), 'date': data['date'], 'days_ahead': days, 'error': err})
        df = pd.concat([df, new], axis=0)

    # Filter out NaN
    df = df[np.isfinite(df['error'])]

    return(df)


def get_population(location):
    locations = pd.read_csv(
        'forecasts/covid19-forecast-hub/data-locations/locations.csv')

    # If location is an abbreviation, convert to name
    if location in abbr_to_state.keys():
        location = abbr_to_state[location]

    return(locations[locations['location_name'] == location]['population'].iat[0])
