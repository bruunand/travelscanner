from datetime import timedelta
from time import sleep

from logging import getLogger

from travelscanner.data.database import Database
from travelscanner.errors import NoCrawlersException
from travelscanner.options.travel_options import TravelOptions


class Agent(object):
    def __init__(self):
        self.crawlers = []
        self.travel_options = TravelOptions()
        self.crawl_interval = timedelta(seconds=1)

    def get_travel_options(self):
        return self.travel_options

    def add_crawler(self, crawler):
        crawler.set_agent(self)
        self.crawlers.append(crawler)

    def set_scanning_interval(self, scan_interval):
        self.crawl_interval = scan_interval

    def crawl(self):
        if len(self.crawlers) == 0:
            raise NoCrawlersException()

        for date in self.get_travel_options().get_dates_in_range():
            previous_travels = set()
            travels = set()

            getLogger().info(f"Current date: {date}")

            for crawler in self.crawlers:
                travels.update(crawler.crawl(date))

            # Ensure that overlapping travels are not saved by saving travels from previous iteration
            Database.save_travels(travels.difference(previous_travels))
            previous_travels = travels

            if self.crawl_interval is not None:
                sleep(self.crawl_interval.total_seconds())
