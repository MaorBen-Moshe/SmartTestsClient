import os
import logging

from flask import Flask
from flask_caching import Cache
from flask.logging import default_handler
from flask_cors import CORS
from flask_executor import Executor
from flask_login import LoginManager
# import flask_monitoringdashboard as dashboard

app_config = {
    'SECRET_KEY': os.urandom(24),
    'CACHE_TYPE': 'FileSystemCache',  # Flask-Caching related configs
    'CACHE_DEFAULT_TIMEOUT': 600,  # 10 minutes
    'CACHE_THRESHOLD': 10,
    'CACHE_DIR': os.path.join(os.path.dirname(__file__), "cache"),
    'EXECUTOR_TYPE': 'thread',
    'EXECUTOR_MAX_WORKERS': 10,
}

app = Flask(__name__)

app.config.from_mapping(app_config)

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

cache_manager = Cache()
cache_manager.init_app(app)

executor_manager = Executor()
executor_manager.init_app(app)

# dashboard.bind(app)

from app.utils import utils
from app.models import config_manager, socket_handler
from app.appLogging import app_logger_manager as alm
from app.appLogging.trace_id_filter import TraceIdFilter

config = config_manager.ConfigManager()
config.init_configs(os.path.dirname(__file__), "config.yaml")

trace_id_filter = TraceIdFilter(utils.Utils.get_request_id)

app.logger.removeHandler(default_handler)
app_logger_manager = alm.AppLoggerManager()
app_logger_manager.init_logger(app.logger,
                               config.get_log_level(),
                               os.path.join(os.path.dirname(__file__), "logs"),
                               config.get_log_file(),
                               trace_id_filter)

app_logger_manager.init_logger(logging.getLogger('werkzeug'),
                               config.get_log_level(),
                               os.path.join(os.path.dirname(__file__), "logs"),
                               config.get_log_file(),
                               trace_id_filter)

app_main_logger = app_logger_manager.get_logger(app.logger.name)

socket_handler = socket_handler.SocketHandler(app)

from app import views
