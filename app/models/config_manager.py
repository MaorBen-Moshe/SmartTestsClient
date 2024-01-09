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
    """A class that manages the configuration settings for the application."""

    __slots__ = ["_fernet", "_config"]

    def __init__(self):
        """Initializes the config manager with None values for the fernet and the config."""
        self._fernet: Fernet | None = None
        self._config = None

    def init_configs(self, config_path: str | None, config_name: str | None):
        """Initializes the config manager with the config file and the encryption key.

        Args:
            config_path (str | None): The path of the config file, or None.
            config_name (str | None): The name of the config file, or None.

        Raises:
            ConfigurationError: If the config path is None.
        """
        if config_path is None:
            raise ConfigurationError("Failed to create configs file. path is None.")

        dotenv.load_dotenv(dotenv_path=os.path.join(config_path, ".env"))

        config_full_path = os.path.join(config_path, config_name)
        with open(config_full_path, "r") as config_file:
            self._config = yaml.safe_load(config_file)
            encrypt_key = os.getenv("encrypt_key")
            self._fernet = Fernet(encrypt_key) if encrypt_key else None

    def get_server_port(self) -> int:
        """Gets the server port from the config.

        Returns:
            int: The server port.
        """
        return self._config["server"]["port"]

    def get_server_host(self) -> str | None:
        """Gets the server host from the config.

        Returns:
            str | None: The server host, or None if not set.
        """
        return self._config["server"]["host"]

    def get_supported_groups(self) -> SupportedGroups:
        """Gets the supported groups from the config.

        Returns:
            SupportedGroups: The supported groups object.
        """
        supported_groups_dict = self._config["app"]["supported_groups"]
        return self.__get_supported_groups_helper(supported_groups_dict)

    def get_supported_services(self, related_group: str | None = None) -> ServicesData:
        """Gets the supported services from the config.

        Args:
            related_group (str | None): The related group to filter the services by, or None to get all services.

        Returns:
            ServicesData: The supported services object.
        """
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
        """Gets the nexus credentials from the config.

        Returns:
            (str, str): The nexus username and password.
        """
        return self.__get_external_cred_by_key("nexus_user", "nexus_password")

    def get_jenkins_cred(self) -> (str, str):
        """Gets the jenkins credentials from the config.

        Returns:
            (str, str): The jenkins username and password.
        """
        return self.__get_external_cred_by_key("jenkins_user", "jenkins_password")

    def get_index_data_repository(self) -> str | None:
        """Gets the index data repository from the config.

        Returns:
            str | None: The index data repository, or None if not set.
        """
        data = self._config["nexus"]["index_data_repository"]
        return data

    def get_nexus_search_url(self) -> str | None:
        """Gets the nexus search URL from the config.

        Returns:
            str | None: The nexus search URL, or None if not set.
        """
        return self._config["nexus"]["nexus_search_endpoint"]

    def get_smart_tests_all_url(self) -> str:
        """Gets the smart tests all URL from the config.

        Returns:
            str: The smart tests all URL.
        """
        return f'{self._config["smart_client"]["base_url"]}{self._config["smart_client"]["smart_tests_all_endpoint"]}'

    def get_smart_tests_statistics_url(self) -> str:
        """Gets the smart tests statistics URL from the config.

        Returns:
            str: The smart tests statistics URL.
        """
        return (f'{self._config["smart_client"]["base_url"]}'
                f'{self._config["smart_client"]["smart_tests_statistics_endpoint"]}')

    @classmethod
    def get_admin_api_token(cls) -> str:
        """Gets the admin API token from the environment variable.

        Returns:
            str: The admin API token.
        """
        return os.getenv("admin_token")

    @classmethod
    def get_user_api_token(cls) -> str:
        """Gets the user API token from the environment variable.

        Returns:
            str: The user API token.
        """
        return os.getenv("user_token")

    def get_log_level(self) -> str:
        """Gets the log level from the config.

        Returns:
            str: The log level, or "INFO" if not set.
        """
        return self._config["logging"]["log_level"] if "log_level" in self._config["logging"] else "INFO"

    def get_log_file(self) -> str:
        """Gets the log file name from the config.

        Returns:
            str: The log file name.
        """
        return self._config["logging"]["log_file_name"]

    def is_get_all_endpoint_cache_enabled(self) -> bool:
        """Checks if the cache is enabled for the get all endpoint.

        Returns:
            bool: True if the cache is enabled, False otherwise.
        """
        return self.__get_is_cache_enabled_by_key("get_all_endpoint")

    def is_smart_analyze_endpoint_cache_enabled(self) -> bool:
        """Checks if the cache is enabled for the smart analyze endpoint.

        Returns:
            bool: True if the cache is enabled, False otherwise.
        """
        return self.__get_is_cache_enabled_by_key("smart_analyze_endpoint")

    def get_get_all_endpoint_cache_ttl(self) -> int:
        """Gets the cache time to live for the get all endpoint.

        Returns:
            int: The cache time to live in seconds, or 0 if not set.
        """
        return self.__get_cache_ttl_by_key("get_all_endpoint")

    def get_smart_analyze_endpoint_cache_ttl(self) -> int:
        """Gets the cache time to live for the smart analyze endpoint.

        Returns:
            int: The cache time to live in seconds, or 0 if not set.
        """
        return self.__get_cache_ttl_by_key("smart_analyze_endpoint")

    def __get_supported_groups_helper(self, supported_groups_str_format: dict[str, Any]) -> SupportedGroups:
        """Helper method that converts a dictionary of supported groups to a SupportedGroups object.

        Args:
            supported_groups_str_format (dict[str, Any]): A dictionary of supported groups.

        Returns:
            SupportedGroups: A SupportedGroups object.
        """
        groups = SupportedGroups()
        for group_name, group in supported_groups_str_format.items():
            if group_name is not None:
                default_supported_groups = self._config["app"]["default_groups_test_files"]
                services_data = self.get_supported_services(group_name)
                groups.add_item(group_name, (SupportedGroup.create().namespace(group_name)
                                             .url(group["url"])
                                             .cluster(group["cluster"])
                                             .test_files(default_supported_groups + group["test_files"])
                                             .services_data(services_data)
                                             .project(group["project"])
                                             .build()))

        return groups

    def __get_external_cred_by_key(self, user_key: str, password_key: str) -> (str, str):
        """Helper method that gets the external credentials from the environment variables and decrypts them if needed.

        Args:
            user_key (str): The key of the user name in the environment variables.
            password_key (str): The key of the password in the environment variables.

        Returns:
            (str, str): The user name and the password.
        """
        user = os.getenv(user_key)
        password = os.getenv(password_key)
        if password:
            if self._fernet:
                password = self._fernet.decrypt(password).decode("utf-8")

        return user, password

    def __get_is_cache_enabled_by_key(self, key: str) -> bool:
        """Helper method that gets the cache enabled flag from the config by the given key.

        Args:
            key (str): The key of the cache enabled flag in the config.

        Returns:
            bool: The cache enabled flag, or False if not set.
        """
        value = self._config["cache"][key]['enabled']
        return bool(value) if value is not None else False

    def __get_cache_ttl_by_key(self, key: str) -> int:
        """Helper method that gets the cache time to live from the config by the given key.

        Args:
            key (str): The key of the cache time to live in the config.

        Returns:
            int: The cache time to live in seconds, or 0 if not set.
        """
        value = self._config["cache"][key]['ttl']
        return int(value) if value is not None else 0
