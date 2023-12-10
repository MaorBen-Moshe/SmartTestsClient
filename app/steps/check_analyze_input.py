from __future__ import annotations

from app.exceptions.excpetions import BadRequest
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.models.supported_group import SupportedGroup


class CheckAnalyzeClientInputStep:

    @staticmethod
    def check_input(parameters: AnalyzeAppServiceParameters | None, supported_groups: dict[str, SupportedGroup]):
        if parameters is None:
            raise BadRequest("No payload provided.")

        if parameters.build_url is None or parameters.build_url == "":
            raise BadRequest("No build url provided.")
        if parameters.group_name not in supported_groups:
            raise BadRequest(f"Group Name: '{parameters.group_name}' is not supported.")
