from __future__ import annotations

from bs4 import BeautifulSoup

from app.clients.html_parser_client import HtmlParserClient
from app.constants.constants import TR, TD, B, TABLE, TABLE_NAME, TABLE_INDEX_NAME_KEY, TABLE_INDEX_VERSION_KEY, \
    TABLE_INDEX_MICROSERVICE_PREFIX
from app.decorators.decorators import log_around
from app.exceptions.excpetions import NotFoundError
from app.models.services_data import ServicesData


class HtmlParserService:
    """A class that parses an HTML file and updates the services map with the versions of the microservices."""

    def __init__(self):
        """Initializes the HTML parser service with None values for the table, the HTML, and the soup."""
        self.table = None
        self.html = None
        self.soup = None

    @log_around(print_output=False)
    def load_html(self,
                  html_zip_url: str | None,
                  services_map: ServicesData | None):
        """Loads the HTML file from the given URL and updates the services map with the versions of the microservices.

        Args:
            html_zip_url (str | None): The URL of the HTML zip file, or None to skip.
            services_map (ServicesData | None): The services map to update, or None to skip.

        Raises:
            NotFoundError: If the HTML file does not contain the expected table.
        """
        if services_map is None or len(services_map) == 0:
            return

        self.html = HtmlParserClient.get_html(html_zip_url)
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.table = self.__find_table()
        if self.table is not None:
            name_index, version_index = self.__find_indexes()
            self.__update_map(services_map, name_index, version_index)
        else:
            raise NotFoundError(f"error with build report structure. not found '{TABLE_NAME}' table")

    def __find_table(self):
        """Finds the table that contains the microservices versions in the HTML file.

        Returns:
            The table element, or None if not found.
        """
        tables = self.soup.find_all(TABLE)
        for table in tables:
            b_element = table.find(TR).find(TD).find(B)
            if b_element is not None and b_element.string == TABLE_NAME:
                return table
        return None

    def __find_indexes(self) -> (int, int):
        """Finds the indexes of the name and version columns in the table.

        Returns:
            (int, int): The indexes of the name and version columns, or None if not found.
        """
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
                     version_index: int):
        """Updates the services map with the versions of the microservices from the table.

        Args:
            services_map (ServicesData): The services map to update.
            name_index (int): The index of the name column in the table.
            version_index (int): The index of the version column in the table.
        """
        rows = self.table.find_all(TR)[2:]  # Skip the first and second rows
        for row in rows:
            cells = row.find_all(TD)
            if cells[name_index] is not None:
                name = cells[name_index].text.split(" ")[0].replace(TABLE_INDEX_MICROSERVICE_PREFIX, "").strip()
                version = cells[version_index].text.strip()
                if len(name) > 0 and len(version) > 0 and name in services_map:
                    if services_map.get_item(name).from_version is None:
                        services_map.get_item(name).from_version = version

                    services_map.get_item(name).to_version = version
