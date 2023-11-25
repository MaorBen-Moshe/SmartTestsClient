from __future__ import annotations

from distutils.version import LooseVersion

from app.clients.yaml_parser_client import YamlParserClient
from app.exceptions.excpetions import EmptyInputError
from app.models.service_data import ServiceData


class YamlParserService:
    def __init__(self):
        self.services_map: dict[str, ServiceData] = {}
        self.yaml_parser_client = YamlParserClient()

    def request_yaml_external(self, urls: list[str] | None, filtered_ms_list: list[str]) -> dict[str, ServiceData]:
        if urls is None:
            raise EmptyInputError("Provided to 'request_yaml_external' None urls list")

        for url in urls:
            data = self.yaml_parser_client.get_yaml(url)

            if data is not None:
                self.__load_yaml(data.get("entries"), filtered_ms_list)

        return self.services_map

    def __load_yaml(self, entries, filtered_ms_list: list[str]):
        if entries is not None:
            for entry in entries:
                try:
                    if entry in filtered_ms_list:
                        version_list = [curr.get('version') for curr in entries.get(entry)]
                        sorted_list = sorted(version_list, key=LooseVersion, reverse=True)
                        if len(sorted_list) > 0:
                            self.services_map[entry] = (ServiceData.create().new_version(sorted_list[0])
                                                        .old_version(sorted_list[0])
                                                        .build())
                except Exception as ex:
                    raise ex
