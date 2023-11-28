import json

import responses
from parameterized import parameterized

from app.clients.nexus_client import NexusClient
from app.exceptions.excpetions import URLError
from test_base import TestBase


class TestNexusClient(TestBase):
    def setUp(self):
        super().setUp()
        self.client = NexusClient()
        self._repo = self.config.get_index_data_repository()

    @responses.activate
    def test_search_data_success(self):
        path = 'http://illin5589:28080/service/rest/v1/search?repository=ms-helm-release&name=productconfigurator'
        with open("resources/nexus_search/configurator_nexus_search_res.json", mode="r") as f:
            responses.add(responses.GET, path, json=json.load(f), status=200)

        params = {"repository": self._repo, "name": "productconfigurator"}
        data = self.client.search_data(params)

        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 2)
        self.assertTrue("items" in data)
        self.assertTrue("continuationToken" in data)

    @parameterized.expand([
        ({"repository": None},),
        ({"Not_Repos": "Not_Repos"},),
        None
    ])
    def test_search_data_wrong_input(self, params):
        self.assert_exception(lambda: self.client.search_data(params),
                              URLError,
                              "Provided to 'search_data' None repository query parameter.")
