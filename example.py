from travelscanner.agent import Agent
from travelscanner.options.travel_options import Airports, Countries
from travelscanner.crawlers.travelmarket import Travelmarket

if __name__ == '__main__':
    agent = Agent()
    options = agent.get_travel_options()

    # Set options for our desired travel
    options.departure_airports = [Airports.AALBORG, Airports.BILLUND, Airports.COPENHAGEN]
    options.destination_countries = [Countries.SPAIN, Countries.GREECE, Countries.CAPE_VERDE, Countries.CROATIA, Countries.CYPRUS, Countries.CROATIA]
    options.set_earliest_departure_date('27/04/2018')
    options.max_price = 10000
    options.number_of_guests = 2

    # Add crawlers
    agent.add_crawler(Travelmarket())

    # Start the agent
    agent.crawl_loop()
