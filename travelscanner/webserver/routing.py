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


@app.route("/price_history/<id>")
def get_price_history(id):
    prices = Price.select().join(Travel).where(Price.travel == id)
    groups = set()
    for test in prices:
        print(test)

    return id


@app.route('/api/get_travels')
def get_travels():
    data = list()

    travels = Travel.select(Travel, fn.Min(Price.price)).limit(1000).join(Price).where(Price.price < 10000).group_by(
        Travel.id)

    for travel in travels:
        country = Countries(travel.country).name

        data.append([travel.id, travel.hotel, travel.area, travel.hotel_stars, country, str(travel.departure_date),
                     travel.duration_days, travel.price])

    return json.dumps({'data': data})
