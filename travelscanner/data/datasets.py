import numpy as np
from sklearn.model_selection import train_test_split

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel
from travelscanner.models.tripadvisor_rating import TripAdvisorRating


def load_unscraped_hotels():
    ret_hotels = []

    # Select distinct hotel names and areas without rating
    travels = Travel.select(Travel.hotel_name, Travel.area, Travel.country).distinct().where(
        TripAdvisorRating.select().where(TripAdvisorRating.hotel_name == Travel.hotel_name,
                                         TripAdvisorRating.area == Travel.area,
                                         TripAdvisorRating.country == Travel.country).count() == 0)
    for travel in travels:
        ret_hotels.append((travel.hotel_name, travel.area))

    return ret_hotels


def load_prices():
    # Get data from database with join query
    joined_prices = Travel.select(Travel, Price).join(Price)

    # Initialize arrays
    n_samples = joined_prices.count()
    features = ["All Inclusive", "Meal type", "Duration (days)", "Country", "Guests", "Hotel stars",
                "Days until departure", "Month", "Week", "Departure airport", "Has pool", "Has childpool",
                "Room type", "Weekday", "Day", "Vendor"]

    data = np.empty((n_samples, len(features)))
    target = np.empty((n_samples,))

    # Fill arrays with data
    for i, d in enumerate(joined_prices):
        # Set features
        data[i] = [d.price.all_inclusive, d.price.meal, d.duration_days, d.country, d.guests, d.hotel_stars,
                   (d.departure_date - d.price.created_at.date()).days, d.departure_date.month,
                   d.departure_date.isocalendar()[1], d.departure_airport, d.has_pool, d.has_childpool, d.price.room,
                   d.departure_date.weekday(), d.departure_date.day, d.vendor]

        # Set target value
        target[i] = d.price.price

    return data, target, features


def split_set(x, y, test_ratio=0.8):
    return train_test_split(x, y, train_size=int(len(x) * test_ratio), random_state=4)
