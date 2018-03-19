from datetime import *

import numpy as np
from sklearn.model_selection import train_test_split

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel


def load_prices():
    today = date.today()

    # Get data from database with join query
    joined_prices = Travel.select(Travel, Price).join(Price)

    # Initialize arrays
    n_samples = joined_prices.count()
    n_features = 13

    data = np.empty((n_samples, n_features))
    target = np.empty((n_samples,))

    # Fill arrays with data
    for i, d in enumerate(joined_prices):
        # Set features
        data[i][0] = d.price.all_inclusive
        data[i][1] = d.price.meal
        data[i][2] = d.duration_days
        data[i][3] = d.country
        data[i][4] = d.guests
        data[i][5] = d.hotel_stars
        data[i][7] = (d.departure_date - today).days  # distance (in days) from current day
        data[i][8] = d.departure_date.month  # todo: is in season?
        data[i][9] = d.departure_date.isocalendar()[1]  # week number
        data[i][10] = d.departure_airport
        data[i][11] = d.has_pool
        data[i][12] = d.price.room

        # Set target value
        target[i] = d.price.price

    return data, target


def split_set(set, test_ratio=0.6):
    x, y = set

    return train_test_split(x, y, train_size=int(len(x) * test_ratio), random_state=4)
