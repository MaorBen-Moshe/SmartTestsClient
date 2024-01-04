from __future__ import annotations

from typing import Iterable

from bs4 import BeautifulSoup

from app.clients.html_parser_client import HtmlParserClient
from app.constants.constants import TR, TD, B, TABLE, TABLE_NAME, TABLE_INDEX_NAME_KEY, TABLE_INDEX_VERSION_KEY, \
    TABLE_INDEX_MICROSERVICE_PREFIX
from app.decorators.decorators import log_around
from app.exceptions.excpetions import NotFoundError
from app.models.service_data import ServiceData
from app.models.services_data import ServicesData


class HtmlParserService:
    def __init__(self):
        self.table = None
        self.html = None
        self.soup = None

    @log_around(print_output=False)
    def load_html(self,
                  html_zip_url: str | None,
                  services_map: ServicesData,
                  group_supported_services: ServicesData):
        self.html = HtmlParserClient.get_html(html_zip_url)
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.table = self.__find_table()
        if self.table is not None:
            name_index, version_index = self.__find_indexes()
            filtered_ms_list = [service for service in group_supported_services]
            self.__update_map(services_map, name_index, version_index, filtered_ms_list, group_supported_services)
        else:
            raise NotFoundError(f"error with build report structure. not found '{TABLE_NAME}' table")

    def __find_table(self):
        tables = self.soup.find_all(TABLE)
        for table in tables:
            b_element = table.find(TR).find(TD).find(B)
            if b_element is not None and b_element.string == TABLE_NAME:
                return table
        return None

    def __find_indexes(self) -> (int, int):
        first_row = self.table.findAll(TR)[1]
        cells = first_row.find_all(TD)
        name_index = None
        version_index = None
        for i, cell in enumerate(cells):
            if cell.text == TABLE_INDEX_NAME_KEY:
                name_index = i
            elif cell.text == TABLE_INDEX_VERSION_KEY:
                version_index = i
        return name_index, version_index

    def __update_map(self,
                     services_map: ServicesData,
                     name_index: int,
                     version_index: int,
                     filtered_ms_list: Iterable[str],
                     group_supported_services: ServicesData):
        rows = self.table.find_all(TR)[2:]  # Skip the first and second rows
        for row in rows:
            cells = row.find_all(TD)
            if cells[name_index] is not None:
                name = cells[name_index].text.split(" ")[0].replace(TABLE_INDEX_MICROSERVICE_PREFIX, "").strip()
                version = cells[version_index].text.strip()
                if len(name) > 0 and len(version) > 0 and name in filtered_ms_list:
                    if name in services_map:
                        services_map.get_item(name).to_version = version
                    else:
                        supported_service_template = group_supported_services.get_item(name)
                        project = supported_service_template.project\
                            if supported_service_template is not None else None
                        repo_name = supported_service_template.repo_name\
                            if supported_service_template is not None else None
                        services_map.add_item(name,
                                              ServiceData.create()
                                              .service_name(name)
                                              .repo_name(repo_name)
                                              .project(project)
                                              .to_version(version)
                                              .from_version(version).build())
