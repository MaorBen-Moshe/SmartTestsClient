import os
from http import HTTPStatus

import flask
from flask import request, jsonify, make_response
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from werkzeug.exceptions import HTTPException

from app import app
from app.appServices.analyze_app_service import AnalyzeAppService
from app.exceptions.excpetions import SmartClientBaseException
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.config_manager import ConfigManager
from app.models.user import User
from app.steps.check_analyze_input import CheckAnalyzeClientInputStep

CORS(app)

config = ConfigManager()
config.init_configs(os.path.join(os.path.dirname(__file__), "config.ini"))

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/health")
@login_required
def health():
    if current_user.is_admin:
        return jsonify({"status": "I'm fine."}), 200
    else:
        flask.abort(HTTPStatus.UNAUTHORIZED)


@app.route("/supported-groups", methods=["GET"])
@login_required
def supported_groups():
    groups = config.get_supported_groups()

    serialized_groups = {group_name: groups[group_name].serialize() for group_name in groups}

    return jsonify(serialized_groups), 200


@app.route("/smart-tests-analyze", methods=["POST"])
@login_required
def analyze():
    groups = config.get_supported_groups()
    req_data = request.get_json()
    CheckAnalyzeClientInputStep.check_input(req_data, groups)
    parameters = (AnalyzeAppServiceParameters
                  .create()
                  .group_name(req_data.get("groupName"))
                  .build_url(req_data.get("buildURL"))
                  .supported_groups(groups)
                  .filtered_ms_list(config.get_filtered_ms_list())
                  .build())

    service = AnalyzeAppService(parameters)

    res = service.analyze()

    return jsonify(res.serialize()), 200


@login_manager.request_loader
def load_user_from_request(req):
    api_key = req.args.get('api_key')
    if api_key:
        if config.get_admin_api_token() == api_key:
            return User.create().is_admin(True).build()
        elif config.get_user_api_token() == api_key:
            return User.create().is_admin(False).build()
        else:
            return None

    return None


@app.errorhandler(Exception)
def handle_exception(ex):
    error_msg = f"[ERROR] {ex}"
    error_code = 500
    if isinstance(ex, SmartClientBaseException):
        error_code = ex.code
    elif isinstance(ex, HTTPException):
        error_code = ex.code

    return make_response(error_msg, error_code)
