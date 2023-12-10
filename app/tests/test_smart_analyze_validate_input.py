from parameterized import parameterized

from app.exceptions.excpetions import BadRequest
from app.models.analyze_app_params import AnalyzeAppServiceParameters
from app.steps.smartAnalyze.smart_analyze_validate_input import SmartAnalyzeValidateInputStep
from test_base import TestUnitBase


class TestSmartAnalyzeValidateInputUnit(TestUnitBase):

    def setUp(self) -> None:
        super().setUp()
        self.step = SmartAnalyzeValidateInputStep()

    def test_check_input_success(self):
        parameters = (AnalyzeAppServiceParameters.create()
                      .build_url("build_url")
                      .group_name("oc-cd-group4")
                      .supported_groups(self.config.get_supported_groups())
                      .build())

        try:
            self.step.execute(parameters)
        except Exception as ex:
            self.fail(f"Error: {ex}")

    @parameterized.expand([
        (None, "No payload provided."),
        (AnalyzeAppServiceParameters.create().build(), "No payload provided."),
        (AnalyzeAppServiceParameters.create().group_name("oc-cd-group4").build(), "No build url provided."),
        (AnalyzeAppServiceParameters.create().build_url("").group_name("oc-cd-group4").build(), "No build url provided."),
        (AnalyzeAppServiceParameters.create().build_url("build_url").build(), f"Group Name: 'None' is not supported."),
        (AnalyzeAppServiceParameters.create().build_url("build_url").group_name("oc-cd-group4_NotSupported").build(),
         f"Group Name: 'oc-cd-group4_NotSupported' is not supported."),
    ])
    def test_check_input_wrong_input(self, parameters, error_msg):
        self.assert_exception(lambda: self.step.execute(parameters),
                              BadRequest,
                              error_msg)
