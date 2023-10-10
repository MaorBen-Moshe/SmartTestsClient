import io
import shutil
import zipfile

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

from constants.constants import *
from exceptions.excpetions import EmptyInputError, NotFoundError
from models.config_manager import ConfigManager
from models.service_data import ServiceData, ServiceDataBuilder


class HtmlParserService:
    def __init__(self, html_zip_url: str):
        self.table = None
        if html_zip_url is None:
            raise EmptyInputError("not provided file_name to load_html")

        self.html = self.__get_html_from_external(html_zip_url)
        self.soup = BeautifulSoup(self.html, "html.parser")

    def load_html(self, services_map: dict[str, ServiceData]):
        self.table = self.__find_table()
        if self.table is not None:
            name_index, version_index = self.__find_indexes()
            self.__update_map(services_map, name_index, version_index)
        else:
            raise NotFoundError("error with build report structure. not found main deployment table")

    def __find_table(self):
        tables = self.soup.find_all("table")
        for table in tables:
            b_element = table.find(TR).find(TD).find(B)
            if b_element is not None and b_element.string == "Main Deployment Steps":
                return table
        return None

    def __find_indexes(self) -> (int, int):
        first_row = self.table.findAll(TR)[1]
        cells = first_row.find_all(TD)
        name_index = None
        version_index = None
        for i, cell in enumerate(cells):
            if cell.text == "Name":
                name_index = i
            elif cell.text == "Current Version":
                version_index = i
        return name_index, version_index

    def __update_map(self, services_map: dict[str, ServiceData], name_index: int, version_index: int):
        rows = self.table.find_all(TR)[2:]  # Skip the first and second rows
        for row in rows:
            cells = row.find_all(TD)
            if cells[name_index] is not None:
                name = cells[name_index].text.split(" ")[0].replace("(Microservice)", "").strip()
                version = cells[version_index].text.strip()
                if len(name) > 0 and len(version) > 0 and name in FILTERED_MS_LIST:
                    if name in services_map:
                        services_map[name].old_version = version
                    else:
                        services_map[name] = ServiceDataBuilder().old_version(version).new_version(version).build()

    @staticmethod
    def __get_html_from_external(html_zip_url: str):
        config = ConfigManager()
        user, password = config.get_jenkins_cred()
        html = None
        with (requests.get(url=html_zip_url,
                           auth=HTTPBasicAuth(user, password))
              as res):
            res.raise_for_status()
            z = zipfile.ZipFile(io.BytesIO(res.content))

            z.extractall("./")
        try:
            with open("./BuildReport/build_report.html", mode="r") as f:
                html = f.read()

        except Exception as ex:
            print(f"Error getting html from {html_zip_url}, with error: {ex}")
            html = None
            raise ex

        finally:
            shutil.rmtree("./BuildReport", ignore_errors=True)
            return html
