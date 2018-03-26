import json

from flask import render_template
from peewee import fn

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel
from travelscanner.options.travel_options import Countries
from travelscanner.webserver import app


@app.route('/')
@app.route('/index')
def frontpage():
    return render_template('index.html')


@app.route('/api/get_travels')
def get_travels():
    data = list()

    travels = Travel.select(Travel, fn.Min(Price.price)).limit(1000).join(Price).where(Price.price < 5000).group_by(Travel.id)

    for travel in travels:
        country = str(Countries(travel.country))

        data.append([travel.hotel, travel.area, travel.hotel_stars, country, str(travel.departure_date),
                     travel.duration_days, travel.price])

    return json.dumps({'data': data})
