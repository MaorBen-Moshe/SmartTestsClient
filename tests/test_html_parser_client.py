from zipfile import BadZipFile

import pytest
import responses
from bs4 import BeautifulSoup

from clients.html_parser_client import HtmlParserClient
from exceptions.excpetions import URLError
from tests.test_base import TestBase


class TestHtmlParserClient(TestBase):

    @responses.activate
    def test_get_html_success(self):
        path = "http://test.com/file.zip"
        with open("resources/html_zip_data.zip", mode="rb") as f:
            responses.add(responses.GET, path, body=f.read(), status=200, content_type="application/zip ")

        html = HtmlParserClient.get_html(path)

        assert bool(BeautifulSoup(html, "html.parser").find())

    @responses.activate
    def test_get_html_empty_body(self):
        path = "http://test.com/file.zip"
        responses.add(responses.GET, path, body="", status=200)

        try:
            HtmlParserClient.get_html(path)
        except BadZipFile as ex:
            assert f"{ex}" == "File is not a zip file"
        except Exception as ex:
            pytest.fail(f"Expected BadZipFile exception, but got: {ex}")
        else:
            pytest.fail("Passed even though the zip response is empty")

    def test_get_html_none_url(self):
        try:
            HtmlParserClient.get_html(None)
        except URLError as err:
            assert f"{err}" == "Build report url: 'None' is not valid."
        except Exception as ex:
            pytest.fail(f"Expected URLError exception, but got: {ex}")
        else:
            pytest.fail("Passed with url None.")
