from __future__ import annotations

import io
import shutil
import zipfile

import requests
import validators
from requests.auth import HTTPBasicAuth

from exceptions.excpetions import URLError
from models.config_manager import ConfigManager


class HtmlParserClient:
    @staticmethod
    def get_html(build_url: str | None):
        if not validators.url(build_url):
            raise URLError(f"Build report url: '{build_url}' is not valid.")

        config = ConfigManager()
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
            print(f"Error getting html from {build_url}, with error: {ex}")
            html = None
            raise ex

        finally:
            shutil.rmtree("./BuildReport", ignore_errors=True)
            return html
