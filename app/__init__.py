import os
import logging

from flask import Flask
from flask.logging import default_handler
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

from app.appLogging import app_logger

app.logger.removeHandler(default_handler)
app_logger.AppLogger.init_logger(app.logger,
                                 config.get_log_level(),
                                 os.path.join(os.path.dirname(__file__), "logs"),
                                 config.get_log_file())

app_logger.AppLogger.init_logger(logging.getLogger('werkzeug'),
                                 config.get_log_level(),
                                 os.path.join(os.path.dirname(__file__), "logs"),
                                 config.get_log_file())

app_main_logger = app_logger.AppLogger.get_logger(app.logger.name)

from app import views
