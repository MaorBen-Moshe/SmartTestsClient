import json

import mock

from constants.constants import GROUP4_XML
from exceptions.excpetions import EmptyInputError
from models.group_data import GroupDataBuilder
from models.service_data import ServiceDataBuilder
from services.smart_test_analyze_service import SmartTestsAnalyzeService
from tests.test_base import TestBase


class TestHandleGroupsDataStep(TestBase):
    def setUp(self):
        super().setUp()
        self.smart_test_analyze_service = SmartTestsAnalyzeService()

        self.get_all_flows_patcher = mock.patch("clients.smart_tests_client.SmartTestsClient.get_all_flows_stats")
        self.mock_get_all_flows = self.get_all_flows_patcher.start()
        self.mock_get_all_flows.side_effect = self.__mock_get_all_flows

        self.analyze_flows_patcher = mock.patch("clients.smart_tests_client.SmartTestsClient.analyze_flows")
        self.mock_analyze_flows = self.analyze_flows_patcher.start()
        self.mock_analyze_flows.side_effect = self.__mock_analyze_flows

    def tearDown(self):
        self.get_all_flows_patcher.stop()
        self.analyze_flows_patcher.stop()

    def test_get_all_flows_by_filter_success(self):
        groups_data = self.smart_test_analyze_service.get_all_flows_by_filter(GROUP4_XML)

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
            "group1": GroupDataBuilder().group_name("group1").group_path("").total_flows_count(10).build(),
            "group2": GroupDataBuilder().group_name("group2").group_path("").total_flows_count(20).build(),
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

    @staticmethod
    def __mock_get_all_flows(*args, **kwargs):
        with open("resources/all_flows_res.json", mode="r") as f:
            return json.load(f)

    @staticmethod
    def __mock_analyze_flows(*args, **kwargs):
        if args[0] == "service1":
            return {
                "flowsCount": 3,
                "flowsByGroupName": [
                    {
                        "name": "/path/group1",
                        "flows": ["flow1", "flow2", "flow3"],
                    },
                ]
            }
        elif args[0] == "service2":
            return {
                "flowsCount": 2,
                "flowsByGroupName": [
                    {
                        "name": "/path/group2",
                        "flows": ["flow1", "flow2"],
                    },
                ]
            }
        else:
            return None
