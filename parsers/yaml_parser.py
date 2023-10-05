from distutils.version import LooseVersion

from constants.constants import *
import yaml
import requests

from models.service_data import ServiceData, ServiceDataBuilder


class YamlParser:
    def __init__(self):
        self.services_map: dict[str, ServiceData] = {}

    def request_yaml_external(self, url: str) -> dict[str, ServiceData]:
        with requests.get(url,
                          auth=(NEXUS_USER, NEXUS_PASS),
                          stream=True) as response:
            response.raise_for_status()
            data = yaml.safe_load(response.content)

        self.load_yaml(data[ENTRIES_KEY])
        return self.services_map

    def load_yaml(self, entries):
        if entries is not None:
            for entry in entries:
                try:
                    if entry in FILTERED_MS_LIST:
                        version_list = [curr['version'] for curr in entries[entry]]
                        sorted_list = sorted(version_list, key=LooseVersion, reverse=True)
                        if len(sorted_list) > 0:
                            if self.services_map.get(entry) is None:
                                self.services_map[entry] = (ServiceDataBuilder().new_version(sorted_list[0])
                                                            .old_version(sorted_list[0])
                                                            .build())
                            else:
                                self.services_map[entry].new_version = sorted_list[0]
                except Exception as ex:
                    raise ex
