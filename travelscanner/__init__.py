from travelscanner.data.database import Database

from travelscanner.models.price import Price
from travelscanner.models.travel import Travel

# Connect to database
Database.connect()

# Create model tables
#Database.get_driver().drop_tables([Price, Travel])
#Database.get_driver().create_tables([Price, Travel])