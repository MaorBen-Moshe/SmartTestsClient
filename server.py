from flask import Flask, request, jsonify, make_response

from appServices.analyze_app_service import AnalyzeAppService
from constants.constants import SUPPORTED_GROUPS
from steps.check_analyze_input import check_input

app = Flask(__name__)


@app.route("/supported-groups", methods=["GET"])
def supported_groups():
    return jsonify(SUPPORTED_GROUPS)


@app.route("/smart-tests-analyze", methods=["POST"])
def analyze():
    try:
        req_data = request.get_json()
        check_input(req_data)
    except Exception as ex:
        return make_response(f"Error: {ex}", 400)

    service = AnalyzeAppService(req_data.get("buildURL"), req_data.get("groupName"))

    res = service.analyze()

    return jsonify(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)  # todo change port to 5000 when running on virtual machine.
