import json

import responses

from constants.constants import GROUP4_XML
from steps.handle_groups_data_step import HandleGroupsDataStep
from tests.test_base import TestBase


class TestHandleGroupsDataStep(TestBase):
    def setUp(self):
        super().setUp()
        self.handle_groups_data_step = HandleGroupsDataStep(None)

    @responses.activate
    def test_init_groups_data_success(self):
        path = self.handle_groups_data_step.client.smart_tests_all_url
        with open("resources/all_flows_res.json", mode="r") as f:
            responses.add(responses.POST, path, json=json.load(f), status=200)

        self.handle_groups_data_step.group_filter = GROUP4_XML
        groups_data = self.handle_groups_data_step.init_groups_data()

        assert len(groups_data) == 2

        assert "mat_APIGW_testng.xml" in groups_data
        mat_groups_data = groups_data.get("mat_APIGW_testng.xml")
        self.assert_group_data(mat_groups_data,
                               'mat_APIGW_testng.xml',
                               'com/amdocs/core/oc/testng',
                               12)

        assert "extended_mat_7b_APIGW_testng.xml" in groups_data
        b2b_groups_data = groups_data.get("extended_mat_7b_APIGW_testng.xml")
        self.assert_group_data(b2b_groups_data,
                               'extended_mat_7b_APIGW_testng.xml',
                               'com/amdocs/core/oc/testng',
                               45)

        assert 'unknown-group' not in groups_data

    @responses.activate
    def test_init_groups_data_emtpy_group_filter(self):
        path = self.handle_groups_data_step.client.smart_tests_all_url
        with open("resources/all_flows_res.json", mode="r") as f:
            responses.add(responses.POST, path, json=json.load(f), status=200)

        self.handle_groups_data_step.group_filter = []

        groups_data = self.handle_groups_data_step.init_groups_data()

        assert len(groups_data) == 3

        assert "mat_APIGW_testng.xml" in groups_data
        mat_groups_data = groups_data.get("mat_APIGW_testng.xml")
        self.assert_group_data(mat_groups_data,
                               'mat_APIGW_testng.xml',
                               'com/amdocs/core/oc/testng',
                               12)

        assert "extended_mat_7b_APIGW_testng.xml" in groups_data
        b2b_groups_data = groups_data.get("extended_mat_7b_APIGW_testng.xml")
        self.assert_group_data(b2b_groups_data,
                               'extended_mat_7b_APIGW_testng.xml',
                               'com/amdocs/core/oc/testng',
                               45)

        assert 'unknown-group' in groups_data
        unknown_groups_data = groups_data.get("unknown-group")
        self.assert_group_data(unknown_groups_data,
                               'unknown-group',
                               '',
                               655)
