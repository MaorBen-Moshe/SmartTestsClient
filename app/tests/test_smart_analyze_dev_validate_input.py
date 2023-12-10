from parameterized import parameterized

from app.exceptions.excpetions import BadRequest
from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters
from app.steps.smartAnalyzeDev.smart_analyze_dev_validate_input import SmartAnalyzeDevValidateInputStep
from app.tests.test_base import TestUnitBase


class TestSmartAnalyzeDevValidateInputUnit(TestUnitBase):

    def setUp(self) -> None:
        super().setUp()
        self.step = SmartAnalyzeDevValidateInputStep()

    @parameterized.expand([
        AnalyzeDevAppServiceParameters.create().services_input([{"name": "service1",
                                                                 "from": "from1"}]).build(),
        AnalyzeDevAppServiceParameters.create().services_input([]).build()
    ])
    def test_check_input_success(self, parameters):
        try:
            self.step.execute(parameters)
            if len(parameters.services_input) > 0:
                self.assertIsNotNone(parameters.data_manager.services_map)
                self.assertEqual(len(parameters.services_input), len(parameters.data_manager.services_map))
                self.assertTrue("service1" in parameters.data_manager.services_map)
                self.assertEqual("from1", parameters.data_manager.services_map["service1"].from_version)
                self.assertEqual(None, parameters.data_manager.services_map["service1"].to_version)
            else:
                self.assertIsNotNone(parameters.data_manager.services_map)
                self.assertEqual(0, len(parameters.data_manager.services_map))
        except Exception as ex:
            self.fail(f"Error: {ex}")

    @parameterized.expand([
        (None, "No payload provided."),
        (AnalyzeDevAppServiceParameters.create().build(),
         "No payload provided."),
        (AnalyzeDevAppServiceParameters.create().services_input(None).build(),
         "No services input provided."),
        (AnalyzeDevAppServiceParameters.create().services_input("services_input").build(),
         "Services input should be a list."),
        (AnalyzeDevAppServiceParameters.create().services_input(["wrong_service"]).build(),
         "Each Service in services should be a dictionary."),
        (AnalyzeDevAppServiceParameters.create().services_input([{"name": "service1"}]).build(),
         "Service is missing mandatory field: 'from'."),
        (AnalyzeDevAppServiceParameters.create().services_input([{"from": "from1"}]).build(),
         "Service is missing mandatory field: 'name'."),
    ])
    def test_check_input_failures(self, parameters, error_msg):
        self.assert_exception(lambda: self.step.execute(parameters),
                              BadRequest,
                              error_msg)
