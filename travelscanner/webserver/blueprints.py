import json

from flask import Blueprint
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel
from travelscanner.models.tripadvisor_rating import TripAdvisorRating
from travelscanner.options.travel_options import Countries, MealTypes, RoomTypes, TravelOptions
from travelscanner.webserver import utils

api_blueprint = Blueprint('simple_page', __name__)


@api_blueprint.route("/price_history/<id>")
def get_price_history(id):
    groups = Price.select(Price.meal, Price.room, Price.all_inclusive).distinct().where(Price.travel == id)

    figure = Figure()
    legends = []
    for group in groups:
        # Add a subplot for each distinct group
        axes = figure.add_subplot(111)

        prices = Price.select().where(Price.travel == id, Price.meal == group.meal, Price.room == group.room,
                                      Price.all_inclusive == group.all_inclusive).order_by(Price.created_at).desc()

        # Add data to subplot
        axes.plot_date([price.created_at for price in prices], [price.price for price in prices], '-')
        axes.xaxis.set_major_formatter(DateFormatter('%d/%m %H:%M'))

        # Add information to legends
        legends.append(f'{MealTypes(group.meal).name}, {RoomTypes(group.room).name}')

    figure.legend(legends, loc='upper left')
    figure.autofmt_xdate()

    # Return plot as image
    return utils.make_response_from_figure(figure)


@api_blueprint.route('/api/get_travels')
def get_travels():
    data = list()

    earlist = TravelOptions.parse_date('29/07/2018')
    latest = TravelOptions.parse_date('29/07/2018')
    countries = [10, 22]

    travels = Travel.select(Travel, Price, TripAdvisorRating).join(TripAdvisorRating, on=(
                (Travel.country == TripAdvisorRating.country) & (Travel.hotel == TripAdvisorRating.hotel) &
                (Travel.area == TripAdvisorRating.area))).switch(Travel).join(Price). \
              where(Travel.hotel_stars > 3 and Travel.departure_date.between(earlist, latest) and Travel.country << countries)

    for travel in travels:
        travel_dict = {
            'country': Countries(travel.country).name,
            'area': travel.area,
            'price': {
                'actual': travel.price.price,
                'predicted': travel.price.predicted_price
            },
            'hotel': {
                'name': travel.hotel,
                'stars': travel.hotel_stars,
                'all_inclusive': travel.price.all_inclusive
            },
            'ratings': travel.tripadvisorrating.rating,
            'duration': travel.duration_days,
            'departure': travel.departure_date.strftime('%d/%m/%Y'),
            'link': travel.price.link,
        }

        data.append(travel_dict)

    return json.dumps(data)
