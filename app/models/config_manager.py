from __future__ import annotations

from typing import Any

import yaml
from cryptography.fernet import Fernet

from app.exceptions.excpetions import ConfigurationError
from app.models.singleton_meta import SingletonMeta
from app.models.supported_group import SupportedGroup
from app.models.supported_groups import SupportedGroups


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        self._fernet: Fernet | None = None
        self._config = None

    def init_configs(self, config_path: str | None):
        if config_path is None:
            raise ConfigurationError("Failed to create configs file. path is None.")

        with open(config_path, "r") as config_file:
            self._config = yaml.safe_load(config_file)
            self._fernet = Fernet(self._config["app"]["encrypt_key"]) if "encrypt_key" in self._config["app"] else None

    def get_server_port(self) -> int:
        return self._config["server"]["port"]

    def get_server_host(self) -> str | None:
        return self._config["server"]["host"]

    def get_supported_groups(self) -> SupportedGroups:
        supported_groups_dict = self._config["app"]["supported_groups"]
        return self.__get_supported_groups_helper(supported_groups_dict)

    def get_nexus_cred(self) -> (str, str):
        nexus_user = None
        nexus_password = None
        if "nexus" in self._config:
            if "nexus_user" in self._config["nexus"]:
                nexus_user = self._config["nexus"]["nexus_user"]
            if "nexus_password" in self._config["nexus"]:
                nexus_password = self._fernet.decrypt(self._config["nexus"]["nexus_password"]).decode("utf-8")

        return nexus_user, nexus_password

    def get_jenkins_cred(self) -> (str, str):
        jenkins_user = None
        jenkins_password = None
        if "jenkins" in self._config:
            if "jenkins_user" in self._config["jenkins"]:
                jenkins_user = self._config["jenkins"]["jenkins_user"]
            if "jenkins_password" in self._config["jenkins"]:
                jenkins_password = self._fernet.decrypt(self._config["jenkins"]["jenkins_password"]).decode("utf-8")

        return jenkins_user, jenkins_password

    def get_index_data_repository(self) -> str | None:
        data = self._config["nexus"]["index_data_repository"]
        return data

    def get_nexus_search_url(self) -> str | None:
        return self._config["nexus"]["nexus_search_endpoint"]

    def get_smart_tests_all_url(self) -> str:
        return f'{self._config["smart_client"]["base_url"]}{self._config["smart_client"]["smart_tests_all_endpoint"]}'

    def get_smart_tests_statistics_url(self) -> str:
        return (f'{self._config["smart_client"]["base_url"]}'
                f'{self._config["smart_client"]["smart_tests_statistics_endpoint"]}')

    def get_admin_api_token(self) -> str:
        return self._config["app"]["admin_token"]

    def get_user_api_token(self) -> str:
        return self._config["app"]["user_token"]

    def get_log_level(self) -> str:
        return self._config["logging"]["log_level"] if "log_level" in self._config["logging"] else "INFO"

    def get_log_file(self) -> str:
        return self._config["logging"]["log_file_name"]

    def get_log_level_by_name(self, name: str) -> str:
        return self._config["logging"][name] if name in self._config["logging"] else self.get_log_level()

    def is_get_all_endpoint_cache_enabled(self) -> bool:
        value = self._config["cache"]["get_all_endpoint"]['enabled']
        return bool(value) if value is not None else False

    def __get_supported_groups_helper(self, supported_groups_str_format: dict[str, Any]) -> SupportedGroups:
        groups = SupportedGroups()
        for group_name, group in supported_groups_str_format.items():
            if group_name is not None:
                default_supported_groups = self._config["app"]["default_groups_test_files"]
                groups.add_item(group_name, (SupportedGroup.create().group_name(group_name)
                                             .url(group["url"])
                                             .cluster(group["cluster"])
                                             .test_files(default_supported_groups + group["test_files"])
                                             .ms_list(group["ms_list"])
                                             .project(group["project"])
                                             .build()))

        return groups
