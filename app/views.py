from datetime import datetime
from http import HTTPStatus

import flask
from flask import request, jsonify, make_response
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException

from app import app, login_manager, config, socket_handler, app_main_logger
from app.appServices.analyze_app_service import AnalyzeAppService
from app.appServices.analyze_dev_app_service import AnalyzeDevAppService
from app.constants.constants import TRACE_ID_HEADER, GROUP_NAME_KEY, BUILD_URL_KEY, INFO_LEVEL_KEY, SERVICES_KEY, \
    API_KEY_QUERY_PARAM, PULL_REQUEST_ID_KEY
from app.enums.res_info_level import ResInfoLevelEnum
from app.exceptions.excpetions import SmartClientBaseException
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.models.error_model import Error
from app.models.user import User
from app.utils.utils import Utils


@app.route("/health")
@login_required
def health():
    if current_user.is_admin:
        resp = make_response(jsonify({"status": "I'm fine."}), 200)
        resp.headers[TRACE_ID_HEADER] = Utils.get_request_id()
        return resp
    else:
        flask.abort(HTTPStatus.UNAUTHORIZED)


@app.route("/supported-groups", methods=["GET"])
@login_required
def supported_groups():
    app_main_logger.debug("Supported groups request.")

    groups = config.get_supported_groups()

    serialized_groups = {group_name: groups.get_item(group_name).serialize() for group_name in groups}

    app_main_logger.debug(f"Supported groups response. response={serialized_groups}")

    resp = make_response(jsonify(serialized_groups), 200)
    resp.headers[TRACE_ID_HEADER] = Utils.get_request_id()
    return resp


@app.route("/smart-tests-analyze", methods=["POST"])
@login_required
def analyze():
    groups = config.get_supported_groups()
    req_data = request.get_json()

    parameters = (AnalyzeAppServiceParameters
                  .create()
                  .group_name(req_data.get(GROUP_NAME_KEY))
                  .build_url(req_data.get(BUILD_URL_KEY))
                  .session_id(Utils.get_session_id_or_default(req_data))
                  .supported_groups(groups)
                  .res_info_level(ResInfoLevelEnum.get_level(req_data.get(INFO_LEVEL_KEY)))
                  .build())

    app_main_logger.debug(f"Smart tests analyze request. parameters={parameters}")

    service = AnalyzeAppService(parameters)

    res = service.analyze()

    app_main_logger.debug(f"Smart tests analyze response. response={res}")

    resp = make_response(jsonify(res.serialize()), 200)
    resp.headers[TRACE_ID_HEADER] = Utils.get_request_id()
    return resp


@app.route("/smart-tests-analyze-dev", methods=["POST"])
@login_required
def analyze_dev():
    req_data = request.get_json()

    parameters = (AnalyzeDevAppServiceParameters.create()
                  .services_input(req_data.get(SERVICES_KEY))
                  .session_id(Utils.get_session_id_or_default(req_data))
                  .res_info_level(ResInfoLevelEnum.get_level(req_data.get(INFO_LEVEL_KEY)))
                  .supported_groups(config.get_supported_groups())
                  .build())

    app_main_logger.debug(f"Smart tests analyze dev request. parameters={parameters}")

    service = AnalyzeDevAppService(parameters)

    res = service.analyze_dev()

    app_main_logger.debug(f"Smart tests analyze dev response. response={res}")

    resp = make_response(jsonify(res.serialize()), 200)
    resp.headers[TRACE_ID_HEADER] = Utils.get_request_id()
    return resp


@login_manager.request_loader
def load_user_from_request(req):
    api_key = req.headers.get(API_KEY_QUERY_PARAM)
    if api_key:
        if config.get_admin_api_token() == api_key:
            return User.create().is_admin(True).build()
        elif config.get_user_api_token() == api_key:
            return User.create().is_admin(False).build()
        else:
            app_main_logger.error(f"Invalid api key header. {API_KEY_QUERY_PARAM}={api_key}")
            return None

    app_main_logger.error(f"Invalid api key header. {API_KEY_QUERY_PARAM}=None")
    return None


@app.errorhandler(Exception)
def handle_exception(ex):
    error_msg = f"[ERROR] {ex}"
    error_code = 500
    if isinstance(ex, SmartClientBaseException):
        error_code = ex.code
    elif isinstance(ex, HTTPException):
        error_code = ex.code

    return make_response((Error.create()
                          .error_message(error_msg)
                          .error_code(error_code)
                          .timestamp(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                          .trace_id(Utils.get_request_id())
                          .build()
                          .serialize()), error_code)


@socket_handler.socketio.on('connect', namespace=socket_handler.namespace)
def handle_socket_connection():
    app_main_logger.info("Socket connection established.")


@socket_handler.socketio.on('disconnect', namespace=socket_handler.namespace)
def handle_socket_disconnection():
    app_main_logger.info("Socket connection disconnected.")


@socket_handler.socketio.on_error_default
def error_handler(e):
    app_main_logger.error(f'SocketErrorHandler: An error has occurred: {e}')
