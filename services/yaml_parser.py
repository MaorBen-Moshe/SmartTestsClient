from distutils.version import LooseVersion

from requests.auth import HTTPBasicAuth

from constants.constants import *
import yaml
import requests

from models.config_manager import ConfigManager
from models.service_data import ServiceData, ServiceDataBuilder


class YamlParserService:
    def __init__(self):
        self.services_map: dict[str, ServiceData] = {}

    def request_yaml_external(self, url: str) -> dict[str, ServiceData]:
        config = ConfigManager()
        user, password = config.get_nexus_cred()
        with requests.get(url,
                          auth=HTTPBasicAuth(user, password),
                          stream=True) as response:
            response.raise_for_status()
            data = yaml.safe_load(response.content)

        self.load_yaml(data.get("entries"))
        return self.services_map

    def load_yaml(self, entries):
        if entries is not None:
            for entry in entries:
                try:
                    if entry in FILTERED_MS_LIST:
                        version_list = [curr.get('version') for curr in entries.get(entry)]
                        sorted_list = sorted(version_list, key=LooseVersion, reverse=True)
                        if len(sorted_list) > 0:
                            if self.services_map.get(entry) is None:
                                self.services_map[entry] = (ServiceDataBuilder().new_version(sorted_list[0])
                                                            .old_version(sorted_list[0])
                                                            .build())
                            else:
                                self.services_map.get(entry).new_version = sorted_list[0]
                except Exception as ex:
                    raise ex
