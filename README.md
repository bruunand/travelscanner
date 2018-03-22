# travelscanner
Last minute travel scanner/crawler for Danish travel agencies and centralised scaners. Mainly a personal research project dedicated to determining prices of last minute travels and playing around with large quantities of data. Intended for running on local machines/servers, **not** for commercial use.

## Current features
- Crawl travels from Travelmarket
- Save travels and associated prices to database, powered by peewee and whichever database driver peewee can support
- Use a regressor to predict travel prices

## Planned features
- Use TripAdvisor to gather additional ratings of hotels, as hotel stars can be misleading
- Use the predicted prices to find actual good offers
- Local webserver showing overview of travels powered by Flask
- Notifications about travels powered by Pushbullet
- Add more crawlers for other Danish websites
