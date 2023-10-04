from distutils.version import LooseVersion

from constants.constants import *
import yaml
import requests


class YamlParser:
    def request_yaml_external(self, url: str, file_name: str, services_map: dict):
        with requests.get(url,
                          auth=(NEXUS_USER, NEXUS_PASS),
                          stream=True) as response:
            response.raise_for_status()
            with open(file_name, "wb") as f:
                f.write(response.content)
            data = yaml.safe_load(response.content)

        self.load_yaml(data[ENTRIES_KEY], services_map)

    def load_yaml(self, entries, services_map):
        if entries is not None:
            for entry in entries:
                try:
                    if entry in FILTERED_MS_LIST:
                        version_list = [curr['version'] for curr in entries[entry]]
                        sorted_list = sorted(version_list, key=LooseVersion, reverse=True)
                        if len(sorted_list) > 0:
                            if services_map.get(entry) is None:
                                services_map[entry] = {OLD_VERSION_KEY: sorted_list[0], NEW_VERSION_KEY: sorted_list[0]}
                            else:
                                services_map[entry][NEW_VERSION_KEY] = sorted_list[0]
                except Exception as ex:
                    raise ex
