from app.exceptions.excpetions import BadRequest
from app.models.supported_group import SupportedGroup


class CheckAnalyzeClientInputStep:

    @staticmethod
    def check_input(req_data, supported_groups: dict[str, SupportedGroup]):
        if req_data is None or len(req_data) == 0:
            raise BadRequest("No payload provided.")

        build_url = req_data.get("buildURL")
        if build_url is None or build_url == "":
            raise BadRequest("No build url provided.")
        group_name = req_data.get("groupName")
        if group_name not in supported_groups:
            raise BadRequest(f"Group Name: '{group_name}' is not supported.")
