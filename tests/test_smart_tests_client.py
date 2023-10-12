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

        assert len(groups_data) == 2
        