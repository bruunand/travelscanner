from travelscanner.agent import Agent
from travelscanner.crawlers.travelmarket import Travelmarket
from travelscanner.data.database import Database
from travelscanner.options.travel_options import Airports

if __name__ == '__main__':
    # Set options for our desired travel
    agent = Agent()
    options = agent.get_travel_options()
    options.departure_airports = [Airports.AALBORG, Airports.BILLUND, Airports.COPENHAGEN]
    options.set_earliest_departure_date('20/06/2018')
    options.number_of_guests = 2
    options.max_days_from_departure = 3

    # Add crawlers
    agent.add_crawler(Travelmarket())

    # Start the agent
    agent.crawl_loop()
