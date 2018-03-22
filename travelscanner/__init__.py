import logging

from travelscanner.data.database import Database

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to database
Database.connect()

# Create model tables
#Database.get_driver().drop_tables([Price, Travel])
#Database.get_driver().create_tables([Price, Travel])

# Initialize cache
logging.getLogger().info("Initializing cache")

for travel in Travel.select():
    Database.retrieve_from_cache(travel)

for price in Price.select():
    Database.retrieve_from_cache(price)

logging.getLogger().info(f"Loaded {len(Database.get_instance().cache)} elements into cache")
