import uuid
from http import HTTPStatus

import flask
from flask import request, jsonify, make_response
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException

from app import app, login_manager, config, socket_handler, app_main_logger
from app.appServices.analyze_app_service import AnalyzeAppService
from app.appServices.analyze_dev_app_service import AnalyzeDevAppService
from app.exceptions.excpetions import SmartClientBaseException
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.user import User


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
    app_main_logger.debug("Supported groups request.")

    groups = config.get_supported_groups()

    serialized_groups = {group_name: groups[group_name].serialize() for group_name in groups}

    app_main_logger.debug(f"Supported groups response. response={serialized_groups}")

    return jsonify(serialized_groups), 200


@app.route("/smart-tests-analyze", methods=["POST"])
@login_required
def analyze():
    groups = config.get_supported_groups()
    req_data = request.get_json()

    parameters = (AnalyzeAppServiceParameters
                  .create()
                  .group_name(req_data.get("groupName"))
                  .build_url(req_data.get("buildURL"))
                  .session_id(req_data.get("sessionID") if req_data.get("sessionID") else uuid.uuid4())
                  .supported_groups(groups)
                  .filtered_ms_list(config.get_filtered_ms_list())
                  .build())

    app_main_logger.debug(f"Smart tests analyze request. parameters={parameters}")

    service = AnalyzeAppService(parameters)

    res = service.analyze()

    app_main_logger.debug(f"Smart tests analyze response. response={res}")

    return make_response(jsonify(res.serialize()), 200)


@app.route("/smart-tests-analyze-dev", methods=["POST"])
@login_required
def analyze_dev():
    req_data = request.get_json()

    parameters = (AnalyzeDevAppServiceParameters.create()
                  .services_input(req_data.get("services"))
                  .session_id(req_data.get("sessionID") if req_data.get("sessionID") else uuid.uuid4())
                  .build())

    app_main_logger.debug(f"Smart tests analyze dev request. parameters={parameters}")

    service = AnalyzeDevAppService(parameters)

    res = service.analyze_dev()

    app_main_logger.debug(f"Smart tests analyze dev response. response={res}")

    return make_response(jsonify(res.serialize()), 200)


@login_manager.request_loader
def load_user_from_request(req):
    api_key = req.args.get('api_key')
    if api_key:
        if config.get_admin_api_token() == api_key:
            return User.create().is_admin(True).build()
        elif config.get_user_api_token() == api_key:
            return User.create().is_admin(False).build()
        else:
            app_main_logger.warning(f"Invalid api key. api_key={api_key}")
            return None

    app_main_logger.warning(f"Invalid api key. api_key=None")
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


@socket_handler.socketio.on('connect', namespace=socket_handler.namespace)
def handle_socket_connection():
    app_main_logger.info("Socket connection established.")


@socket_handler.socketio.on('disconnect', namespace=socket_handler.namespace)
def handle_socket_disconnection():
    app_main_logger.info("Socket connection disconnected.")


@socket_handler.socketio.on_error_default
def error_handler(e):
    app_main_logger.error(f'SocketErrorHandler: An error has occurred: {e}')
