# travelscanner
Last minute travel scanner for Danish travel agencies and scanners. Mainly a research project dedicated to determining prices of last minute travels. Intended for running on local machines/servers, not designed for commercial use.

## Current features
- Crawl travels from Travelmarket
- Save travels and associated prices to database, powered by peewee and whichever database driver peewee can support

## Planned features
- Use TripAdvisor to gather additional ratings of hotels, as hotel stars can be misleading
- Use a regressor to predict hotel prices and use the predicted prices to find actual good offers
- Local webserver showing overview of travels powered by Flask
- Notifications about travels powered by Pushbullet
- Add more crawlers for other Danish websites
