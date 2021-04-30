import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np

import utils

import forecasts.COVIDhubensemble as forecast
import truth.CSSE as truth

# Choose a location
loc = "US"

# Load truth_data
truth_df = truth.load(location=loc)


# Load all forecasts and compute relative errors
###############################################################################
dates = forecast.list_dates()
error_df = utils.compute_error_all_forecasts(
    forecast, truth_df,
    utils.rel_err,
    field='cumDeaths',
    dates=dates,
    location=loc)


# Plot error quantiles vs forcast days ahead
###############################################################################
fig, ax = plt.subplots()

# Maximum number of days ahead to consider
days_ahead = 28
error_flt = error_df[error_df['days_ahead'] < days_ahead]

# Compute quantiles
q25 = error_flt.groupby('days_ahead')['error'].quantile(q=0.25)
q50 = error_flt.groupby('days_ahead')['error'].quantile(q=0.50)
q75 = error_flt.groupby('days_ahead')['error'].quantile(q=0.75)

ax.plot(q50.keys(), q50)
plt.fill_between(q50.keys(), q25, q75, color='gray', alpha=0.2)

ax.set_xlabel('Forecasted days ahead')
ax.set_ylabel('Median Percentage Error')
ax.yaxis.set_major_formatter(PercentFormatter(1))
plt.tight_layout()
plt.show()


# Plot MAPE of each forecast through time
##############################################################################
fig, ax = plt.subplots()

# Selected completed forecasts
error_df = error_df[error_df['forecast_completed'] == True]

# Plot MAPE
error_df['error'] = np.abs(error_df['error'])
df_error_mean = error_df.groupby('forecast_date')['error'].mean()
ax.scatter(df_error_mean.keys(), df_error_mean)

# Plot 7-day moving average of daily deaths
ax_r = ax.twinx()
truth_date = truth_df['date'][6:]
truth_deaths = utils.moving_avg(truth_df['deaths'], 7)
ax_r.plot(truth_date, truth_deaths, color='black')

# Plot holidays
truth_dict = dict(zip(truth_date, truth_deaths))
for h in utils.holidays.keys():
    date = utils.holidays[h]
    ax_r.vlines(date, 0, truth_dict[date], ls='--', color='gray')

# format the ticks
utils.xaxis_months(fig, ax)

ax.set_ylim(bottom=0)
ax.set_xlabel("Forecast date")
ax.set_ylabel("Mean Absolute Percentage Error")
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax_r.set_ylim(bottom=0)
ax_r.set_ylabel("Daily Deaths")
plt.tight_layout()
plt.show()
