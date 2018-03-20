from datetime import timedelta
from time import sleep

from logging import getLogger

from travelscanner.errors import NoCrawlersException
from travelscanner.options.travel_options import TravelOptions


class Agent(object):
    def __init__(self):
        self.crawlers = []
        self.travel_options = TravelOptions()
        self.crawl_interval = timedelta(minutes=5)

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
                getLogger().info(f"Saving {len(travels)} travels")

                for i, travel in enumerate(travels):
                    travel.upsert()

                    if i % 10 == 0:
                        getLogger().info(f"{(i+1) / len(travels) * 100}% saved")

                getLogger().info(f"Saving complete")

                sleep(self.crawl_interval.total_seconds())
