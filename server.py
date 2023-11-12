import os

from flask import Flask, request, jsonify, make_response
from werkzeug.exceptions import HTTPException

from appServices.analyze_app_service import AnalyzeAppService
from exceptions.excpetions import SmartClientBaseException
from models.analyze_app_params import AnalyzeAppServiceParametersBuilder
from models.config_manager import ConfigManager
from steps.check_analyze_input import CheckAnalyzeClientInputStep

app = Flask(__name__)
config = ConfigManager()


@app.route("/health")
def health():
    return jsonify({"status": "I'm fine."}), 200


@app.route("/supported-groups", methods=["GET"])
def supported_groups():
    groups = config.get_supported_groups()

    serialized_groups = {group_name: groups[group_name].serialize() for group_name in groups}

    return jsonify(serialized_groups), 200


@app.route("/smart-tests-analyze", methods=["POST"])
def analyze():
    try:
        groups = config.get_supported_groups()
        req_data = request.get_json()
        CheckAnalyzeClientInputStep.check_input(req_data, groups)
        parameters = (AnalyzeAppServiceParametersBuilder().group_name(req_data.get("groupName"))
                                                          .build_url(req_data.get("buildURL"))
                                                          .supported_groups(groups)
                                                          .filtered_ms_list(config.get_filtered_ms_list())
                                                          .build())

        service = AnalyzeAppService(parameters)

        res = service.analyze()

    except SmartClientBaseException as ex:
        return make_response(f"{ex}", ex.code)
    except HTTPException as ex:
        return make_response(f"[ERROR] {ex}", ex.code)
    except Exception as ex:
        return make_response(f"[ERROR] {ex}", 500)
    else:
        return jsonify(res.serialize()), 200


if __name__ == '__main__':
    dir_name = os.path.dirname(__file__)
    config.init_configs(os.path.join(dir_name, "config.ini"))
    app.run(host="0.0.0.0", port=5001)
