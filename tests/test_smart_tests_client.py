import json

import responses

from clients.smart_tests_client import SmartTestsClient
from constants.constants import GROUP4_XML
from tests.test_base import TestBase
from utils.utils import Utils


class TestSmartTestsClient(TestBase):

    def setUp(self):
        super().setUp()
        self.client = SmartTestsClient()

    @responses.activate
    def test_get_all_flows_stats_success(self):
        path = self.client.smart_tests_all_url
        with open("resources/all_flows_res.json", mode="r") as f:
            responses.add(responses.POST, path, json=json.load(f), status=200)

        groups_data = self.client.get_all_flows_stats(Utils.create_filter_by_list(GROUP4_XML))

        self.assertEqual(len(groups_data), 2)

    @responses.activate
    def test_analyze_flows(self):
        path = self.client.smart_tests_statistics_url
        with open("resources/smart_stats.json", mode="r") as f:
            responses.add(responses.POST, path, json=json.load(f), status=200)

        res_json = self.client.analyze_flows("productcofigurator",
                                             "0.67.18",
                                             "0.67.19",
                                             "")

        self.assertIn("flowsCount", res_json)
        self.assertEqual(res_json["flowsCount"], 10)
        self.assertIn("flowsByGroupName", res_json)
        self.assertIsInstance(res_json["flowsByGroupName"], list)
        groups = res_json["flowsByGroupName"]
        self.assertEqual(len(groups), 1)
        group = groups[0]
        self.assertIsNotNone(group)
        self.assertIn("name", group)
        self.assertEqual(group["name"], "mat_APIGW_testng.xml")
        self.assertIn("flows", group)
        self.assertIsInstance(group["flows"], list)
        flows = group["flows"]
        self.assertEqual(len(flows), 2)
        self.assertIn("flow1", flows)
        self.assertIn("flow2", flows)
