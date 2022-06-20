from flask import Flask, Blueprint
from flask_cors import CORS

from api.settings import API_PREFIX
from api.endpoints import init

# init flask app
app = Flask(__name__)


# blueprints
bp = Blueprint('api', __name__, url_prefix=API_PREFIX)  # api's blueprint
bp.register_blueprint(init.blueprint)
app.register_blueprint(bp)

# cors
CORS(app)
