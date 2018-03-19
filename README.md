# travelscanner
Last minute travel scanner for Danish travel agencies and scanners.

## Current features
- Crawl travels from Travelmarket
- Save travels and associated prices to database, powered by peewee and whichever database driver peewee can support

## Planned features
- Use TripAdvisor to gather additional ratings of hotels, as hotel stars can be misleading
- Use a regressor to predict hotel prices and use the predicted prices to find actual good offers
- Local webserver powered by Flask, showing overview of travels
- Notifications powered by Pushbullet
- Add more crawlers for other Danish websites
