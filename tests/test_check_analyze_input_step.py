from exceptions.excpetions import BadRequest
from steps.check_analyze_input import CheckAnalyzeClientInputStep
from test_base import TestUnitBase


class TestCheckAnalyzeInputUnit(TestUnitBase):
    def test_check_input_success(self):

        req_data = {
            "buildURL": "build_url",
            "groupName": "oc-cd-group4-coc-include-ed",
        }

        try:
            CheckAnalyzeClientInputStep.check_input(req_data, self.config.get_supported_groups())
        except Exception as ex:
            self.fail(f"Error: {ex}")

    def test_check_input_input_is_none(self):
        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(None,
                                                                              self.config.get_supported_groups()),
                              BadRequest,
                              "No payload provided.")

    def test_check_input_input_is_empty_dict(self):
        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input({},
                                                                              self.config.get_supported_groups()),
                              BadRequest,
                              "No payload provided.")

    def test_check_input_input_is_build_url_none(self):
        data = {
            "groupName": "oc-cd-group4-coc-include-ed",
        }

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(data,
                                                                              self.config.get_supported_groups()),
                              BadRequest,
                              "No build url provided.")

    def test_check_input_input_is_build_url_empty(self):
        data = {
            "buildURL": "",
            "groupName": "oc-cd-group4-coc-include-ed",
        }

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(data,
                                                                              self.config.get_supported_groups()),
                              BadRequest,
                              "No build url provided.")

    def test_check_input_input_is_group_name_none(self):
        data = {
            "buildURL": "build_url",
        }

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(data, self.config.get_supported_groups()),
                              BadRequest,
                              f"Group Name: 'None' is not supported. supported groups:"
                              f" {self.config.get_supported_groups()}")

    def test_check_input_input_is_group_name_not_supported(self):
        data = {
            "buildURL": "build_url",
            "groupName": "oc-cd-group4-coc-include-ed_NotSupported"
        }

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(data, self.config.get_supported_groups()),
                              BadRequest,
                              (f"Group Name: 'oc-cd-group4-coc-include-ed_NotSupported' is not supported. supported "
                              f"groups: {self.config.get_supported_groups()}"))
