from exceptions.excpetions import EmptyInputError
from models.group_data import GroupDataBuilder
from models.service_data import ServiceDataBuilder
from services.smart_test_analyze_service import SmartTestsAnalyzeService
from tests.test_base import TestUnitBase


class TestHandleGroupsDataStepUnit(TestUnitBase):
    def setUp(self):
        super().setUp()
        self.smart_test_analyze_service = SmartTestsAnalyzeService()

    def test_get_all_flows_by_filter_success(self):
        group4_xml = self.config.get_supported_groups().get('oc-cd-group4-coc-include-ed').testng_xml
        groups_data = self.smart_test_analyze_service.get_all_flows_by_filter(group4_xml)

        self.mock_get_all_flows.assert_called()
        self.assertEqual(len(groups_data), 2)

        self.assertIn("mat_APIGW_testng.xml", groups_data)
        mat_groups_data = groups_data.get("mat_APIGW_testng.xml")
        self.assert_group_data(mat_groups_data,
                               'mat_APIGW_testng.xml',
                               'com/amdocs/core/oc/testng',
                               12)

        self.assertIn("extended_mat_7b_APIGW_testng.xml", groups_data)
        b2b_groups_data = groups_data.get("extended_mat_7b_APIGW_testng.xml")
        self.assert_group_data(b2b_groups_data,
                               'extended_mat_7b_APIGW_testng.xml',
                               'com/amdocs/core/oc/testng',
                               45)

        self.assertNotIn('unknown-group', groups_data)

    def test_get_all_flows_by_filter_emtpy_group_filter(self):
        groups_data = self.smart_test_analyze_service.get_all_flows_by_filter([])

        self.mock_get_all_flows.assert_called()
        self.assertEqual(len(groups_data), 3)

        self.assertIn("mat_APIGW_testng.xml", groups_data)
        mat_groups_data = groups_data.get("mat_APIGW_testng.xml")
        self.assert_group_data(mat_groups_data,
                               'mat_APIGW_testng.xml',
                               'com/amdocs/core/oc/testng',
                               12)

        self.assertIn("extended_mat_7b_APIGW_testng.xml", groups_data)
        b2b_groups_data = groups_data.get("extended_mat_7b_APIGW_testng.xml")
        self.assert_group_data(b2b_groups_data,
                               'extended_mat_7b_APIGW_testng.xml',
                               'com/amdocs/core/oc/testng',
                               45)

        self.assertIn('unknown-group', groups_data)
        unknown_groups_data = groups_data.get("unknown-group")
        self.assert_group_data(unknown_groups_data,
                               'unknown-group',
                               '',
                               655)

    def test_analyze_flows_success(self):
        services_map = {
            "service1": ServiceDataBuilder().old_version("1.0").new_version("2.0").build(),
            "service2": ServiceDataBuilder().old_version("3.0").new_version("4.0").build()
        }
        filter_group = ["group1", "group2"]
        groups_data = {
            "group1": GroupDataBuilder().test_xml_name("group1").test_xml_path("").total_flows_count(10).build(),
            "group2": GroupDataBuilder().test_xml_name("group2").test_xml_path("").total_flows_count(20).build(),
        }

        self.smart_test_analyze_service.analyze_flows(services_map, filter_group, groups_data)

        self.assertEqual(self.mock_analyze_flows.call_count, 2)
        self.assertEqual(groups_data["group1"].curr_flows_count, 3)
        self.assertListEqual(groups_data["group1"].flows, ["flow1", "flow2", "flow3"])
        self.assertEqual(groups_data["group2"].curr_flows_count, 2)
        self.assertListEqual(groups_data["group2"].flows, ["flow1", "flow2"])

    def test_analyze_flows_no_services_map(self):
        self.assert_exception(lambda: self.smart_test_analyze_service.analyze_flows(None,
                                                                                    [],
                                                                                    {}),
                              EmptyInputError,
                              "failed to fetch flows to analyze. no services or groups data found.")

        self.mock_analyze_flows.assert_not_called()
