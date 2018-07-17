from flask import Flask
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from travelscanner.webserver.blueprints import ts_blueprint

app = Flask(__name__)

# Setup bootstrap
CORS(app)
Bootstrap(app)

# Setup routing
app.register_blueprint(ts_blueprint)
