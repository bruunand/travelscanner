from flask import Flask
from flask_cors import CORS
from travelscanner.webserver.blueprints import api_blueprint

app = Flask(__name__)

# Setup bootstrap
CORS(app)

# Setup routing
app.register_blueprint(api_blueprint)