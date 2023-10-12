import pytest
import responses

from clients.yaml_parser_client import YamlParserClient
from exceptions.excpetions import URLError
from tests.test_base import TestBase


class TestYamlParserClient(TestBase):
    def setUp(self):
        super().setUp()
        self.client = YamlParserClient()

    @responses.activate
    def test_get_yaml_success(self):
        path = "http://test.com/yaml"
        with open("resources/index.yaml", mode="r") as f:
            responses.add(responses.GET, path, body=f.read(), status=200)

        data = self.client.get_yaml(path)

        assert type(data) is dict
        assert len(data) == 3
        assert "entries" in data

    def test_get_yaml_wrong_url(self):
        path = "not_valid_url"

        try:
            data = self.client.get_yaml(path)
        except URLError as ex:
            assert f"{ex}" == "Yaml url: 'not_valid_url' is not valid."
        else:
            pytest.fail("client.get_yaml passed with not valid url.")

    def test_get_yaml_none_url(self):
        try:
            data = self.client.get_yaml(None)
        except URLError as ex:
            assert f"{ex}" == "Yaml url: 'None' is not valid."
        else:
            pytest.fail("client.get_yaml passed with None url.")
