from constants.constants import SUPPORTED_GROUPS
from exceptions.excpetions import BadRequest
from steps.check_analyze_input import CheckAnalyzeClientInputStep
from tests.test_base import UnitTestBase


class TestCheckAnalyzeInput(UnitTestBase):
    def test_check_input_success(self):

        req_data = {
            "buildURL": "build_url",
            "groupName": SUPPORTED_GROUPS[0],
        }

        try:
            CheckAnalyzeClientInputStep.check_input(req_data)
        except Exception as ex:
            self.fail(f"Error: {ex}")

    def test_check_input_input_is_none(self):
        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(None),
                              BadRequest,
                              "No payload provided.")

    def test_check_input_input_is_empty_dict(self):
        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input({}),
                              BadRequest,
                              "No payload provided.")

    def test_check_input_input_is_build_url_none(self):
        data = {
            "groupName": SUPPORTED_GROUPS[0],
        }

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(data),
                              BadRequest,
                              "No build url provided.")

    def test_check_input_input_is_build_url_empty(self):
        data = {
            "buildURL": "",
            "groupName": SUPPORTED_GROUPS[0],
        }

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(data),
                              BadRequest,
                              "No build url provided.")

    def test_check_input_input_is_group_name_none(self):
        data = {
            "buildURL": "build_url",
        }

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(data),
                              BadRequest,
                              f"Group Name: 'None' is not supported. supported groups: {SUPPORTED_GROUPS}")

    def test_check_input_input_is_group_name_not_supported(self):
        data = {
            "buildURL": "build_url",
            "groupName": SUPPORTED_GROUPS[0] + "_NotSupported"
        }

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(data),
                              BadRequest,
                              (f"Group Name: '{SUPPORTED_GROUPS[0] + '_NotSupported'}' is not supported. supported "
                              f"groups: {SUPPORTED_GROUPS}"))
