import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

import utils
import forecasts.IHME as forecast
import truth.CSSE as truth


# Choose a location
loc = "US"

# Plot forecasts onto truth data
###############################################################################
fig, ax = plt.subplots()

# Plot truth
truth_df = truth.load(location=loc)
ax.plot(truth_df['date'], truth_df['cumDeaths'],
        linewidth=2, color='black', label='Actual')

# Plot forecasts
forecast_dates = forecast.list_dates()
for date in forecast_dates:
    forecast_df = forecast.load(date, location=loc)
    mask = np.isfinite(forecast_df['cumDeaths'])  # Filter out NaN
    ax.plot(forecast_df['date'][mask],
            forecast_df['cumDeaths'][mask], linestyle='--')

# format the ticks
utils.xaxis_months(fig, ax)

ax.set_xlim(left=datetime(2020, 3, 1))
ax.set_title(utils.get_location_string(loc))
ax.set_xlabel('Date')
ax.set_ylabel('Deaths')
ax.legend()
plt.tight_layout()
plt.show()
