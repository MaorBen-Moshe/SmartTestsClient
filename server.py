from flask import Flask, request, jsonify

from appServices.analyze_app_service import AnalyzeAppService
from constants.constants import SUPPORTED_GROUPS
from exceptions.excpetions import BadRequest

app = Flask(__name__)


@app.route("/supported-groups", methods=["GET"])
def supported_groups():
    return jsonify(SUPPORTED_GROUPS)


@app.route("/smart-tests-analyze", methods=["POST"])
def analyze():
    req_data = request.get_json()
    if req_data is None:
        raise BadRequest("No payload provided.")

    build_url = req_data.get("buildURL")
    if build_url is None or build_url == "":
        raise BadRequest("No build url provided.")
    group_name = req_data.get("groupName")
    if group_name not in SUPPORTED_GROUPS:
        raise BadRequest(f"Group Name: {group_name} is not supported. supported groups: {SUPPORTED_GROUPS}")

    service = AnalyzeAppService(build_url, group_name)

    return jsonify(service.analyze())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)  # todo change port to 5000 when running on virtual machine.
