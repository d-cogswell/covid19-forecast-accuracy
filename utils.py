import numpy as np
import matplotlib.dates as mdates


def moving_avg(x, N):
    return(np.convolve(x, np.ones((N,))/N, mode='valid'))


def xaxis_months(fig, ax):
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    fig.autofmt_xdate()
