import matplotlib.pyplot as plt
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

# Compute quantiles
q25 = error_df.groupby('days_ahead')['error'].quantile(q=0.25)
q50 = error_df.groupby('days_ahead')['error'].quantile(q=0.50)
q75 = error_df.groupby('days_ahead')['error'].quantile(q=0.75)

ax.plot(q50.keys(), q50)
plt.fill_between(q50.keys(), q25, q75, color='gray', alpha=0.2)

ax.set_xlabel('Forecasted days ahead')
ax.set_ylabel('Median Percentage Error')

plt.show()


# Plot MAPE of each forecast through time
##############################################################################
fig, ax = plt.subplots()

error_df['error'] = np.abs(error_df['error'])
df_error_mean = error_df.groupby('forecast_date')['error'].mean()
ax.scatter(df_error_mean.keys(), df_error_mean)

ax_r = ax.twinx()
ax_r.plot(truth_df['date'][6:], utils.moving_avg(
    truth_df['deaths'], 7), color='black')

# format the ticks
utils.xaxis_months(fig, ax)

ax.set_xlabel("Forecast date")
ax.set_ylabel("Mean Absolute Percentage Error")
ax_r.set_ylabel("Daily Deaths")
plt.show()
