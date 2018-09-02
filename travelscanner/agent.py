from travelscanner.data.database import Database
from travelscanner.errors import NoCrawlersException
from travelscanner.options.travel_options import TravelOptions


class Agent(object):
    def __init__(self):
        self.crawlers = []
        self.travel_options = TravelOptions()

    def get_travel_options(self):
        return self.travel_options

    def add_crawler(self, crawler):
        crawler.set_agent(self)
        self.crawlers.append(crawler)

    def crawl(self):
        if len(self.crawlers) == 0:
            raise NoCrawlersException()

        date_range = self.get_travel_options().get_dates_in_range()
        travels = set()

        for crawler in self.crawlers:
            travels.update(crawler.crawl(date_range))

        Database.save_travels(travels)
