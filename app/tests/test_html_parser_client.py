from zipfile import BadZipFile

import responses
from bs4 import BeautifulSoup

from app.clients.html_parser_client import HtmlParserClient
from app.exceptions.excpetions import URLError
from test_base import TestBase


class TestHtmlParserClient(TestBase):

    @responses.activate
    def test_get_html_success(self):
        path = "http://test.com/file.zip"
        with open("resources/html_zip_data.zip", mode="rb") as f:
            responses.add(responses.GET, path, body=f.read(), status=200, content_type="application/zip ")

        html = HtmlParserClient.get_html(path)

        self.assertTrue(bool(BeautifulSoup(html, "html.parser").find()))

    @responses.activate
    def test_get_html_empty_body(self):
        path = "http://test.com/file.zip"
        responses.add(responses.GET, path, body="", status=200)

        self.assert_exception(lambda: HtmlParserClient.get_html(path), BadZipFile, "File is not a zip file")

    def test_get_html_none_url(self):
        self.assert_exception(lambda: HtmlParserClient.get_html(None),
                              URLError,
                              "Build report url: 'None' is not valid.")
