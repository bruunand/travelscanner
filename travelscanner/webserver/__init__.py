from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# Setup bootstrap
Bootstrap(app)

# Setup routing
from travelscanner.webserver import routing
