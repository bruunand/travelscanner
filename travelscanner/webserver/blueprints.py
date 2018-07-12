import json

from flask import Blueprint
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from peewee import fn

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel
from travelscanner.options.travel_options import Countries, MealTypes, RoomTypes
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

    travels = Travel.select(Travel, fn.Min(Price.price)).limit(1000).join(Price).where(Price.price < 10000).group_by(
        Travel.id)

    for travel in travels:
        country = Countries(travel.country).name

        data.append([travel.id, travel.hotel, travel.area, travel.hotel_stars, country, str(travel.departure_date),
                     travel.duration_days, travel.price])

    return json.dumps({'data': data})
