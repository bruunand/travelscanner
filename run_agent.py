from travelscanner.agent import Agent
from travelscanner.crawlers.travelmarket import Travelmarket
from travelscanner.options.travel_options import Airports

if __name__ == '__main__':
    # Set options for our desired travel
    agent = Agent()
    options = agent.get_travel_options()
    options.departure_airports = [Airports.AALBORG, Airports.BILLUND, Airports.COPENHAGEN]
    options.set_latest_departure_date('30/11/2018')
    options.number_of_guests = 2

    # Add crawlers
    agent.add_crawler(Travelmarket())

    # Start the agent
    agent.crawl_loop()
