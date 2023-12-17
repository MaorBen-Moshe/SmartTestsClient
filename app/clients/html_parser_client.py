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
    @classmethod
    @gateway_errors_handler
    @log_around(print_output=True)
    def get_html(cls, build_url: str | None):
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
