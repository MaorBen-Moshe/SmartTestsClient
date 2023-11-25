from __future__ import annotations

from configparser import ConfigParser

from cryptography.fernet import Fernet

from app.exceptions.excpetions import ConfigurationError
from app.models.singleton_meta import SingletonMeta
from app.models.supported_group import SupportedGroup, SupportedGroupBuilder


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        self._fernet: Fernet | None = None
        self._config = ConfigParser()

    def init_configs(self, config_path: str | None):
        if config_path is None:
            raise ConfigurationError("Failed to create configs file. path is None.")

        self._config.read(config_path)
        self._fernet = Fernet(self._config["DEFAULT"]["key"])

    def get_supported_groups(self) -> dict[str, SupportedGroup]:
        supported_groups_str = self._config["DEFAULT"]["supported_groups"]
        return self.__get_supported_groups_helper(supported_groups_str)

    def get_filtered_ms_list(self) -> list[str]:
        filtered_ms_list_str = self._config["DEFAULT"]["filtered_ms_list"]
        return filtered_ms_list_str.split(",") if filtered_ms_list_str is not None else []

    def get_nexus_cred(self) -> (str, str):
        return (self._config["NEXUS"]["nexus_user"],
                self._fernet.decrypt(self._config["NEXUS"]["nexus_password"]).decode("utf-8"))

    def get_jenkins_cred(self) -> (str, str):
        return (self._config["JENKINS"]["jenkins_user"],
                self._fernet.decrypt(self._config["JENKINS"]["jenkins_password"]).decode("utf-8"))

    def get_index_data_urls(self) -> list[str]:
        data = self._config["NEXUS"]["index_data_urls"]
        return [val.strip() for val in data.split(",")] if data is not None else []

    def get_smart_tests_all_url(self) -> str:
        return self._config["SMART_CLIENT"]["smart_tests_all"]

    def get_smart_tests_statistics_url(self) -> str:
        return self._config["SMART_CLIENT"]["smart_tests_statistics"]

    def get_admin_api_token(self) -> str:
        return self._config["API"]["admin_token"]

    def get_user_api_token(self) -> str:
        return self._config["API"]["user_token"]

    def __get_supported_groups_helper(self, supported_groups_str_format: str) -> dict[str, SupportedGroup]:
        groups = {}
        testng_xml_per_group = self.__get_testng_xml_per_group_helper(self._config["DEFAULT"]["testng_xml_per_group"])
        if supported_groups_str_format:
            split_supported_groups = supported_groups_str_format.split(",")
            for supported_group in split_supported_groups:
                group_name, cluster, url = supported_group.strip().split("|")
                if group_name is not None:
                    testng_xml = testng_xml_per_group.get(group_name, [])
                    groups[group_name] = (SupportedGroupBuilder().group_name(group_name)
                                                                 .url(url)
                                                                 .cluster(cluster)
                                                                 .testng_xml(testng_xml)
                                                                 .build())

        return groups

    @staticmethod
    def __get_testng_xml_per_group_helper(testng_xml_per_group_str: str) -> dict[str, list[str]]:
        testng_xml_per_group = {}
        if testng_xml_per_group_str:
            split_testng_xml_per_group = testng_xml_per_group_str.split(",")
            for testng_xml in split_testng_xml_per_group:
                group_name, testng_xml_str_format = testng_xml.strip().split(":")
                if group_name is not None:
                    testng_xml = testng_xml_str_format.split("|")
                    if testng_xml is not None:
                        testng_xml_per_group[group_name] = testng_xml

        return testng_xml_per_group
