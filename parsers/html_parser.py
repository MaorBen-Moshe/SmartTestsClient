from bs4 import BeautifulSoup
from constants.constants import *
from exceptions.emptyInputError import EmptyInputError
from exceptions.notFoundError import NotFoundError


class HtmlParser:
    def __init__(self, html):
        self.table = None
        if html is None:
            raise EmptyInputError("not provided file_name to load_html")

        self.soup = BeautifulSoup(html, "html.parser")

    def load_html(self, services_map):
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

    def __find_indexes(self):
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

    def __update_map(self, services_map, name_index, version_index):
        rows = self.table.find_all(TR)[2:]  # Skip the first and second rows
        for row in rows:
            cells = row.find_all(TD)
            if cells[name_index] is not None:
                name = cells[name_index].text.split(" ")[0].replace("(Microservice)", "").strip()
                version = cells[version_index].text.strip()
                if len(name) > 0 and len(version) > 0 and name in FILTERED_MS_LIST:
                    if name in services_map:
                        services_map[name][OLD_VERSION_KEY] = version
                    else:
                        services_map[name] = {OLD_VERSION_KEY: version, NEW_VERSION_KEY: version}
