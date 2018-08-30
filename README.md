# travelscanner
Last minute travel scanner/crawler for Danish travel agencies and centralised scaners. Mainly a personal research project dedicated to determining prices of last minute travels and playing around with large quantities of data. Intended for running on local machines/servers, **not** intended for commercial use.

## Current features
- Crawl travels from Travelmarket and Afbudsrejser
- Save travels and associated prices to database (supports whichever database drivers peewee supports)
- Use a regressor to predict travel prices (XGBoost, several models have been tested)
- Use a TripAdvisor scraper to gather additional ratings of hotels
- Use the predicted prices to find actual good offers

## Roadmap
- Notifications about travels powered by Pushbullet
- Add more crawlers for other Danish websites/scrap centralised scanners
- A webservice providing meaningful statistics into travels as well as highlighting travels with high value for money

## Development history
- 0.1 (current): The system is capable of scanning from two centralized scanners. It is able to construct a model of prices based on observed prices and able to predict prices of unobserved travels. 
