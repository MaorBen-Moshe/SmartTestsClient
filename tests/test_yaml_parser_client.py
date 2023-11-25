import responses

from clients.yaml_parser_client import YamlParserClient
from exceptions.excpetions import URLError
from test_base import TestBase


class TestYamlParserClient(TestBase):
    def setUp(self):
        super().setUp()
        self.client = YamlParserClient()

    @responses.activate
    def test_get_yaml_success(self):
        path = "http://test.com/index.yaml"
        with open("resources/index.yaml", mode="r") as f:
            responses.add(responses.GET, path, body=f.read(), status=200)

        data = self.client.get_yaml(path)

        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 3)
        self.assertTrue("entries" in data)

    def test_get_yaml_wrong_url(self):
        path = "not_valid_url"

        self.assert_exception(lambda: self.client.get_yaml(path),
                              URLError,
                              "Yaml url: 'not_valid_url' is not valid.")

    def test_get_yaml_none_url(self):
        self.assert_exception(lambda: self.client.get_yaml(None),
                              URLError,
                              "Yaml url: 'None' is not valid.")
