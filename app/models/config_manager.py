from __future__ import annotations

from typing import Any

import os

import dotenv
import yaml
from cryptography.fernet import Fernet

from app.constants.constants import SERVICE_PROJECT_KEY, SERVICE_RELATED_GROUP_KEY, SERVICE_REPO_LABEL_KEY
from app.exceptions.excpetions import ConfigurationError
from app.models.service_data import ServiceData
from app.models.services_data import ServicesData
from app.models.singleton_meta import SingletonMeta
from app.models.supported_group import SupportedGroup
from app.models.supported_groups import SupportedGroups


class ConfigManager(metaclass=SingletonMeta):

    __slots__ = ["_fernet", "_config"]

    def __init__(self):
        self._fernet: Fernet | None = None
        self._config = None

    def init_configs(self, config_path: str | None, config_name: str | None):
        if config_path is None:
            raise ConfigurationError("Failed to create configs file. path is None.")

        dotenv.load_dotenv(dotenv_path=os.path.join(config_path, ".env"))

        config_full_path = os.path.join(config_path, config_name)
        with open(config_full_path, "r") as config_file:
            self._config = yaml.safe_load(config_file)
            encrypt_key = os.getenv("encrypt_key")
            self._fernet = Fernet(encrypt_key) if encrypt_key else None

    def get_server_port(self) -> int:
        return self._config["server"]["port"]

    def get_server_host(self) -> str | None:
        return self._config["server"]["host"]

    def get_supported_groups(self) -> SupportedGroups:
        supported_groups_dict = self._config["app"]["supported_groups"]
        return self.__get_supported_groups_helper(supported_groups_dict)

    def get_supported_services(self, related_group: str | None = None) -> ServicesData:
        supported_services_dict = self._config["app"]["supported_services"]

        filtered_supported_services_dict = filter(lambda curr_service_name: related_group is None or
                                                  len(related_group) == 0 or
                                                  supported_services_dict[curr_service_name][SERVICE_RELATED_GROUP_KEY]
                                                  == related_group, supported_services_dict)

        services_data = ServicesData()
        for service_name in filtered_supported_services_dict:
            if service_name is not None:
                service = supported_services_dict[service_name]
                services_data.add_item(service_name, (ServiceData.create()
                                                      .service_name(service_name)
                                                      .repo_name(service[SERVICE_REPO_LABEL_KEY])
                                                      .related_group(service[SERVICE_RELATED_GROUP_KEY])
                                                      .project(service[SERVICE_PROJECT_KEY])
                                                      .build()))
        return services_data

    def get_nexus_cred(self) -> (str, str):
        return self.__get_external_cred_by_key("nexus_user", "nexus_password")

    def get_jenkins_cred(self) -> (str, str):
        return self.__get_external_cred_by_key("jenkins_user", "jenkins_password")

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

    @classmethod
    def get_admin_api_token(cls) -> str:
        return os.getenv("admin_token")

    @classmethod
    def get_user_api_token(cls) -> str:
        return os.getenv("user_token")

    def get_log_level(self) -> str:
        return self._config["logging"]["log_level"] if "log_level" in self._config["logging"] else "INFO"

    def get_log_file(self) -> str:
        return self._config["logging"]["log_file_name"]

    def get_log_level_by_name(self, name: str) -> str:
        return self._config["logging"][name] if name in self._config["logging"] else self.get_log_level()

    def is_get_all_endpoint_cache_enabled(self) -> bool:
        return self.__get_is_cache_enabled_by_key("get_all_endpoint")

    def is_smart_analyze_endpoint_cache_enabled(self) -> bool:
        return self.__get_is_cache_enabled_by_key("smart_analyze_endpoint")

    def get_get_all_endpoint_cache_ttl(self) -> int:
        return self.__get_cache_ttl_by_key("get_all_endpoint")

    def get_smart_analyze_endpoint_cache_ttl(self) -> int:
        return self.__get_cache_ttl_by_key("smart_analyze_endpoint")

    def __get_supported_groups_helper(self, supported_groups_str_format: dict[str, Any]) -> SupportedGroups:
        groups = SupportedGroups()
        for group_name, group in supported_groups_str_format.items():
            if group_name is not None:
                default_supported_groups = self._config["app"]["default_groups_test_files"]
                services_data = self.get_supported_services(group_name)
                groups.add_item(group_name, (SupportedGroup.create().group_name(group_name)
                                             .url(group["url"])
                                             .cluster(group["cluster"])
                                             .test_files(default_supported_groups + group["test_files"])
                                             .services_data(services_data)
                                             .project(group["project"])
                                             .build()))

        return groups

    def __get_external_cred_by_key(self, user_key: str, password_key: str) -> (str, str):
        user = os.getenv(user_key)
        password = os.getenv(password_key)
        if password:
            if self._fernet:
                password = self._fernet.decrypt(password).decode("utf-8")

        return user, password

    def __get_is_cache_enabled_by_key(self, key: str) -> bool:
        value = self._config["cache"][key]['enabled']
        return bool(value) if value is not None else False

    def __get_cache_ttl_by_key(self, key: str) -> int:
        value = self._config["cache"][key]['ttl']
        return int(value) if value is not None else 0
