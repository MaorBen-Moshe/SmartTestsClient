import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import config_manager, socket_handler

config = config_manager.ConfigManager()
config.init_configs(os.path.join(os.path.dirname(__file__), "config.ini"))

socket_handler = socket_handler.SocketHandler(app)

from app import views
