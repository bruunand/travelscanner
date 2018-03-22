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

    def crawl_loop(self):
        if len(self.crawlers) == 0:
            raise NoCrawlersException()

        while True:
            travels = set()

            for crawler in self.crawlers:
                travels.update(crawler.crawl())

            if self.crawl_interval is None:
                break
            else:
                Database.save_travels(travels)

                # Increase next crawl date
                options = self.get_travel_options()
                if options.max_days_from_departure is not None:
                    options.increase_earliest_departure_date(timedelta(days=options.max_days_from_departure))

                getLogger().info(f"Set new earliest departure date to {options.earliest_departure_date}")

                # Wait before crawling again
                sleep(self.crawl_interval.total_seconds())
