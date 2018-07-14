import pickle
import traceback
from logging import getLogger

from travelscanner.agent import Agent
from travelscanner.crawlers.afbudsrejser import Afbudsrejser
from travelscanner.crawlers.travelmarket import Travelmarket
from travelscanner.learning import predictor
from travelscanner.options.travel_options import Airports
from travelscanner.tripadvisor.scraper import Scraper


if __name__ == '__main__':
    # Set options for our desired travel
    agent = Agent()
    options = agent.get_travel_options()
    options.departure_airports = [Airports.AALBORG, Airports.BILLUND, Airports.COPENHAGEN]
    options.set_earliest_departure_date('23/08/2018')
    options.set_latest_departure_date('01/10/2018')
    options.number_of_guests = 2

    # Add crawlers
    agent.add_crawler(Afbudsrejser())
    agent.add_crawler(Travelmarket())

    # Initialize TA scraper
    scraper = Scraper()

    # Run actions in loop
    actions = [agent.crawl, scraper.scrape]#, predictor.predict_prices]
    while True:
        for action in actions:
            try:
                action()
            except Exception as e:
                getLogger().error(traceback.format_exc())
