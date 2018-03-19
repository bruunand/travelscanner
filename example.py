from travelscanner.agent import Agent
from travelscanner.options.travel_options import Airports, Countries
from travelscanner.crawlers.travelmarket import Travelmarket

if __name__ == '__main__':
    agent = Agent()

    # Set options for our desired travel
    options = agent.get_travel_options()
    options.departure_airports = [Airports.AALBORG, Airports.BILLUND, Airports.COPENHAGEN]
    options.destination_countries = None#[Countries.SPAIN, Countries.GREECE, Countries.CAPE_VERDE, Countries.CROATIA, Countries.CYPRUS, Countries.CROATIA]
    options.set_earliest_departure_date('27/04/2018')
    options.max_price = 5000
    options.number_of_guests = 2
    options.duration_days = None
    options.maximum_days_from_departure = 21

    # Add crawlers
    agent.add_crawler(Travelmarket())

    # Start the agent
    agent.crawl_loop()
