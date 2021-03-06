import matplotlib.pyplot as plt

import utils
import truth.CSSE as truth


# Choose a location
loc = "US"

# Load truth data
truth_df = truth.load(location=loc)


# Plot 7-day moving averages
###############################################################################
fig, ax = plt.subplots()
ax_r = ax.twinx()

# Plot 7-day moving averages
ax.plot(truth_df['date'][6:], utils.moving_avg(
    truth_df['deaths'], 7), label='Daily deaths', color='C0')
ax_r.plot(truth_df['date'][6:], utils.moving_avg(
    truth_df['cumDeaths'], 7), label='Cumulative deaths', color='C1')

# Set the x-axis labels to months
utils.xaxis_months(fig, ax)

ax.set_title(utils.get_location_string(loc))
ax.set_xlabel('Date')
ax.set_ylabel("Daily Deaths")
ax_r.set_ylabel("Cumulative Deaths")
fig.legend(loc="upper left", bbox_to_anchor=(
    0, 1), bbox_transform=ax.transAxes)
plt.tight_layout()
plt.show()
