import matplotlib.pyplot as plt

import utils

import forecasts.COVIDhubensemble as forecast
import truth.CSSE as truth

# Choose a location
loc = "US"

# Load truth_data
truth_df = truth.load(location=loc)


# Load forecasts and compute errors
###############################################################################
dates = forecast.list_dates()
error_df = utils.compute_error_all_forecasts(
    forecast, truth_df['date'],
    truth_df['cumDeaths'],
    utils.abs_rel_err,
    dates=dates,
    location=loc)


# Plot error vs forcast days ahead
###############################################################################
fig, ax = plt.subplots()

error_mean = error_df.groupby('days_ahead')['error'].mean()
ax.plot(error_mean.keys(), error_mean)

error_std = error_df.groupby('days_ahead')['error'].std()
plt.fill_between(error_mean.keys(),
                 error_mean.values - error_std.values,
                 error_mean.values + error_std.values,
                 color='gray', alpha=0.2)

ax.set_xlabel('Forecasted days ahead')
ax.set_ylabel('Mean Absolute Percentage Error')

plt.show()


# Plot error of each forecast through time
##############################################################################
fig, ax = plt.subplots()

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
