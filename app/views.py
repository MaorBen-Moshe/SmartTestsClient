import time
import uuid
from http import HTTPStatus

import flask
from flask import request, jsonify, make_response
from flask_login import login_required, current_user
from flask_socketio import emit
from werkzeug.exceptions import HTTPException

from app import app, login_manager, config, socket_handler
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
    groups = config.get_supported_groups()

    serialized_groups = {group_name: groups[group_name].serialize() for group_name in groups}

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

    service = AnalyzeAppService(parameters)

    res = service.analyze()

    return make_response(jsonify(res.serialize()), 200)


@app.route("/smart-tests-analyze-dev", methods=["POST"])
@login_required
def analyze_dev():
    req_data = request.get_json()

    parameters = (AnalyzeDevAppServiceParameters.create()
                  .services_input(req_data.get("services"))
                  .session_id(req_data.get("sessionID") if req_data.get("sessionID") else uuid.uuid4())
                  .build())

    service = AnalyzeDevAppService(parameters)

    res = service.analyze_dev()

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


@socket_handler.socketio.on(socket_handler.internal_event_name, namespace=socket_handler.namespace)
def handle_socket_event(data):
    emit(socket_handler.event_name,
         data,
         broadcast=True,
         callback=lambda x: print(f"Sent {data}."),
         namespace=socket_handler.namespace)


@socket_handler.socketio.on_error_default
def error_handler(e):
    print(f'[ERROR] [{time.localtime().strftime("%Y/%m/%d %H:%M:$S")}] An error has occurred: {e}')
