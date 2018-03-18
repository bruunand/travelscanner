from travelscanner.options.travel_options import Airports
from travelscanner.crawlers.crawler import Crawler, log_on_failure, Crawlers


class Spies(Crawler):
    def __init__(self):
        super().__init__()

        self.airport_dictionary = {Airports.AALBORG: "503274", Airports.BILLUND: "499708",
                                   Airports.COPENHAGEN: "500055"}

    def get_id(self):
        return Crawlers.SPIES

    @log_on_failure
    def crawl(self):
        pass