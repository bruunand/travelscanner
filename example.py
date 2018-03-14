from agent import Agent
from model.travel_options import Airports, Countries
from scanners.travelmarket import TravelMarketScanner

agent = Agent()
options = agent.get_travel_options()

# Set options for our desired travel
options.departure_airports = [Airports.AALBORG, Airports.BILLUND, Airports.COPENHAGEN]
options.destination_countries = [Countries.SPAIN, Countries.GREECE]
options.set_earliest_departure_date('27/04/2018')
options.max_price = 10000
options.number_of_guests = 2

# Add scanners
agent.add_scanner(TravelMarketScanner())

# Start the agent
agent.scan_loop()
