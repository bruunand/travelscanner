import json

from flask import Blueprint, render_template

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel
from travelscanner.models.tripadvisor_rating import TripAdvisorRating
from travelscanner.options.travel_options import Countries, TravelOptions

ts_blueprint = Blueprint('travelscanner', __name__, static_folder='static')


@ts_blueprint.route('/')
@ts_blueprint.route('/index')
def frontpage():
    return render_template('index.html')


@ts_blueprint.route('/api/get_travels')
def get_travels():
    earlist = TravelOptions.parse_date('29/07/2018')
    latest = TravelOptions.parse_date('08/08/2018')

    data = list()

    travels = Travel.select(Travel, Price, TripAdvisorRating).join(TripAdvisorRating, on=(
            (Travel.country == TripAdvisorRating.country) & (Travel.hotel == TripAdvisorRating.hotel) &
            (Travel.area == TripAdvisorRating.area))).switch(Travel).join(Price). \
        where(Travel.hotel_stars > 3 & Travel.departure_date.between(earlist, latest)).limit(5000)

    for travel in travels:
        country = Countries(travel.country).name.title()

        ratio = None
        if travel.price.predicted_price is not None:
            ratio = travel.price.predicted_price / travel.price.price

        data.append([travel.id, travel.price.link, travel.hotel, travel.area, travel.hotel_stars,
                     travel.tripadvisorrating.rating, country, str(travel.departure_date),
                     travel.duration_days, travel.price.price, travel.price.predicted_price, ratio])

    return json.dumps({'data': data})
