from travelscanner.agent import Agent
from travelscanner.crawlers.travelmarket import Travelmarket
from travelscanner.options.travel_options import Airports

if __name__ == '__main__':
    agent = Agent()

    # Set options for our desired travel
    options = agent.get_travel_options()
    options.departure_airports = [Airports.AALBORG, Airports.BILLUND, Airports.COPENHAGEN]
    options.destination_countries = None
    options.set_earliest_departure_date('01/08/2018')
    options.max_price = 15000
    options.number_of_guests = 2
    options.duration_days = None
    options.maximum_days_from_departure = 7

    # Add crawlers
    agent.add_crawler(Travelmarket())

    # Start the agent
    agent.crawl_loop()
