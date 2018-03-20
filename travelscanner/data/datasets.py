from datetime import *

import numpy as np
from sklearn.model_selection import train_test_split

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel


def load_prices():
    today = date.today()

    # Get data from database with join query
    joined_prices = Travel.select(Travel, Price).join(Price).where(Price.price < 15000)

    # Initialize arrays
    n_samples = joined_prices.count()
    n_features = 15

    data = np.empty((n_samples, n_features))
    target = np.empty((n_samples,))

    # Fill arrays with data
    for i, d in enumerate(joined_prices):
        # Set features
        data[i] = [d.price.all_inclusive, d.price.meal, d.duration_days, d.country, d.guests, d.hotel_stars,
                   (d.departure_date - today).days, d.departure_date.month, d.departure_date.isocalendar()[1],
                   d.departure_airport, d.has_pool, d.price.room, d.departure_date.weekday, d.departure_date.day]

        # Set target value
        target[i] = d.price.price

    return data, target, n_features


def split_set(x, y, test_ratio=0.6):
    return train_test_split(x, y, train_size=int(len(x) * test_ratio), random_state=4)
