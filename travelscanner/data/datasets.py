from datetime import *

import numpy as np
from sklearn.utils import Bunch

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel


def load_prices():
    today = date.today()

    # Get data from database with join query
    joint_prices = Travel.select(Travel, Price).join(Price)

    # Initialize arrays
    n_samples = joint_prices.count()
    n_features = 9

    data = np.empty((n_samples, n_features))
    target = np.empty((n_samples,))

    # Fill arrays with data
    for i, d in enumerate(joint_prices):
        # Set features
        data[i][0] = d.price.all_inclusive
        data[i][1] = d.price.meal
        data[i][2] = d.duration_days
        data[i][3] = d.country
        data[i][4] = d.guests
        data[i][5] = d.hotel_stars
        data[i][7] = (d.departure_date - today).days
        data[i][8] = d.departure_date.month

        # Set target value
        target[i] = d.price.price

    return Bunch(data=data, target=target)
