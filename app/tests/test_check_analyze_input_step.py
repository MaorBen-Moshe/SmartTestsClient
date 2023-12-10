from parameterized import parameterized

from app.exceptions.excpetions import BadRequest
from app.models.analyze_app_params import AnalyzeAppServiceParameters, AnalyzeAppServiceParametersBuilder
from app.steps.check_analyze_input import CheckAnalyzeClientInputStep
from test_base import TestUnitBase


class TestCheckAnalyzeInputUnit(TestUnitBase):
    def test_check_input_success(self):
        parameters = (AnalyzeAppServiceParametersBuilder()
                      .build_url("build_url")
                      .group_name("oc-cd-group4")
                      .build())

        try:
            CheckAnalyzeClientInputStep.check_input(parameters, self.config.get_supported_groups())
        except Exception as ex:
            self.fail(f"Error: {ex}")

    def test_check_input_input_is_none(self):
        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(None,
                                                                              self.config.get_supported_groups()),
                              BadRequest,
                              "No payload provided.")

    def test_check_input_input_is_empty_dict(self):
        self.assert_exception(
            lambda: CheckAnalyzeClientInputStep.check_input(AnalyzeAppServiceParametersBuilder().build(),
                                                            self.config.get_supported_groups()),
            BadRequest,
            "No payload provided.")

    @parameterized.expand([
        None,
        ""
    ])
    def test_check_input_input_is_build_url_empty(self, build_url):
        parameters = (AnalyzeAppServiceParametersBuilder()
                      .build_url(build_url)
                      .group_name("oc-cd-group4")
                      .build())

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(parameters,
                                                                              self.config.get_supported_groups()),
                              BadRequest,
                              "No build url provided.")

    @parameterized.expand([
        None,
        "oc-cd-group4_NotSupported"
    ])
    def test_check_input_input_wrong_group_name(self, group_name):
        parameters = (AnalyzeAppServiceParametersBuilder()
                      .build_url("build_url")
                      .group_name(group_name)
                      .build())

        self.assert_exception(lambda: CheckAnalyzeClientInputStep.check_input(parameters,
                                                                              self.config.get_supported_groups()),
                              BadRequest,
                              f"Group Name: '{group_name}' is not supported. supported groups:"
                              f" {self.config.get_supported_groups()}")
