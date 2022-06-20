import os
from flask import Flask, Blueprint
from flask_restplus import Api
from dotenv import load_dotenv

from src.controller.ping import api_ping
from src.controller.user import api_user
from src.controller.users import api_users
from src.controller.auth import api_auth
from src.config import app_config, api_settings
from flask_cors import CORS

load_dotenv()
env_mode = os.getenv('FLASK_ENV', 'dev')

# auth
authorizations = {
    'accessToken': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

# creating flask api
api_v1 = Blueprint(
    'api', __name__,
    url_prefix=api_settings.API_PREFIX
)

api = Api(api_v1,
          authorizations=authorizations,
          version=api_settings.API_VERSION,
          title=api_settings.API_NAME,
          description='User API')

api.add_namespace(api_ping)
api.add_namespace(api_user)
api.add_namespace(api_users)
api.add_namespace(api_auth)

app = Flask(__name__)
CORS(app,
     origins="*",
     allow_headers=["Content-Type", "Authorization",
                    "Access-Control-Allow-Credentials"],
     supports_credentials=True
     )
app.config.from_object(app_config[env_mode])

app.register_blueprint(api_v1)


def init():
    app.run(host=api_settings.API_HOST, debug=True)
