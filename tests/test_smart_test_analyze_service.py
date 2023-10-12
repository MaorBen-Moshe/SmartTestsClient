import json

import pytest
import responses

from constants.constants import GROUP4_XML
from services.smart_test_analyze_service import SmartTestsAnalyzeService
from tests.test_base import TestBase


class TestHandleGroupsDataStep(TestBase):
    def setUp(self):
        super().setUp()
        self.smart_test_analyze_service = SmartTestsAnalyzeService()

    @responses.activate
    def test_get_all_flows_by_filter_success(self):
        path = self.smart_test_analyze_service.client.smart_tests_all_url
        with open("resources/all_flows_res.json", mode="r") as f:
            responses.add(responses.POST, path, json=json.load(f), status=200)

        groups_data = self.smart_test_analyze_service.get_all_flows_by_filter(GROUP4_XML)

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

    @responses.activate
    def test_get_all_flows_by_filter_emtpy_group_filter(self):
        path = self.smart_test_analyze_service.client.smart_tests_all_url
        with open("resources/all_flows_res.json", mode="r") as f:
            responses.add(responses.POST, path, json=json.load(f), status=200)

        groups_data = self.smart_test_analyze_service.get_all_flows_by_filter([])

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

    @pytest.mark.skip(reason="need to implement")
    def test_analyze_flows_success(self):
        pass

    @pytest.mark.skip(reason="need to implement")
    def test_analyze_flows_no_services_map(self):
        pass

    @pytest.mark.skip(reason="need to implement")
    def test_analyze_flows_no_groups_data(self):
        pass

    @pytest.mark.skip(reason="need to implement")
    def test_analyze_flows_empty_input(self):
        pass
