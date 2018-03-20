import logging

from travelscanner.data.database import Database

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to database
Database.connect()

# Initialize cache
for travel in Travel.select():
    Database.get_cache().add(travel)

for price in Price.select():
    Database.get_cache().add(price)

# Create model tables
#Database.get_driver().drop_tables([Price, Travel])
#Database.get_driver().create_tables([Price, Travel])