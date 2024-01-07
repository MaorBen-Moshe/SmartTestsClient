from __future__ import annotations

import io
import shutil
import zipfile

import requests
from requests.auth import HTTPBasicAuth

from app import config
from app.decorators.decorators import gateway_errors_handler, log_around
from app.exceptions.excpetions import URLError
from app.utils.utils import Utils


class HtmlParserClient:
    """A class that parses HTML from a build report URL."""

    @classmethod
    @gateway_errors_handler
    @log_around(print_output=True)
    def get_html(cls, build_url: str | None):
        """Gets the HTML content from a build report URL.

        Args:
            build_url (str | None): The build report URL to get the HTML from, or None.

        Returns:
            str: The HTML content, or None if the URL is not valid or an error occurs.

        Raises:
            URLError: If the URL is not valid or has an unsupported extension.
            BadGatewayError: If any other exception occurs while getting or parsing the HTML.
        """
        if not Utils.is_valid_url(build_url):
            raise URLError(f"Build report url: '{build_url}' is not valid.")

        user, password = config.get_jenkins_cred()
        html = None
        with (requests.get(url=build_url,
                           auth=HTTPBasicAuth(user, password))
              as res):
            res.raise_for_status()
            z = zipfile.ZipFile(io.BytesIO(res.content))

            z.extractall("./")
        try:
            with open("./BuildReport/build_report.html", mode="r") as f:
                html = f.read()
        except Exception as ex:
            raise ex

        finally:
            shutil.rmtree("./BuildReport", ignore_errors=True)
            return html
