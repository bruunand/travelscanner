import json

from flask import Blueprint, render_template

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel
from travelscanner.models.tripadvisor_rating import TripAdvisorRating
from travelscanner.options.travel_options import Countries, TravelOptions, Airports

ts_blueprint = Blueprint('travelscanner', __name__, static_folder='static')


@ts_blueprint.route('/')
@ts_blueprint.route('/index')
def frontpage():
    return render_template('index.html')


@ts_blueprint.route('/api/get_travels')
def get_travels():
    earlist = TravelOptions.parse_date('01/08/2019')
    latest = TravelOptions.parse_date('13/08/2019')

    data = list()

    banned_areas = ['Puerto Rico', 'Playa Del Ingles', 'Madrid', 'Puerto de la Cruz', 'Las Palmas by', 'Gran Canaria',
                    'Playa de las Americas']

    travels = Travel.select(Travel, Price, TripAdvisorRating).join(TripAdvisorRating, on=(
            (Travel.country == TripAdvisorRating.country) & (Travel.hotel == TripAdvisorRating.hotel) &
            (Travel.area == TripAdvisorRating.area))).switch(Travel).join(Price). \
        where((Travel.hotel_stars >= 3) & (Travel.departure_date.between(earlist, latest)) & (Travel.duration_days >= 7)). \
        where((Price.price < 5000) & (Travel.country << [Countries.GREECE, Countries.SPAIN, Countries.CYPRUS])). \
        where(~(Travel.area << banned_areas))

    for travel in travels:
        country = Countries(travel.country).name.title()
        airport = Airports(travel.departure_airport).name.title()

        ratio = None
        if travel.price.predicted_price is not None:
            ratio = travel.price.predicted_price / travel.price.price

        data.append([travel.id, travel.price.link, travel.hotel, travel.price.meal, travel.price.room, travel.area,
                     travel.hotel_stars, travel.tripadvisorrating.rating, travel.distance_beach,
                     airport, country, str(travel.departure_date),
                     travel.duration_days, travel.price.price, travel.price.predicted_price, ratio])

    return json.dumps({'data': data})


    #travels = Travel.select(Travel, Price).join(Price). \
    #    where((Travel.hotel_stars >= 3) & (Travel.country << [Countries.GREECE, Countries.CYPRUS])). \
    #    where((Price.price.between(3000, 4500)) & (Travel.departure_date.between(earliest, latest))). \
    #    where((Price.meal << [MealTypes.BREAKFAST, MealTypes.FULL_BOARD, MealTypes.HALF_BOARD])). \
    #    where((Travel.duration_days >= 7)).\