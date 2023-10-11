from __future__ import annotations

from configparser import ConfigParser
from cryptography.fernet import Fernet

from exceptions.excpetions import ConfigurationError
from models.singleton_meta import SingletonMeta


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        self.__fernet: Fernet | None = None
        self.config = ConfigParser()

    def init_configs(self, config_path: str | None):
        if config_path is None:
            raise ConfigurationError("Failed to create configs file. path is None.")

        self.config.read(config_path)
        self.__fernet = Fernet(self.config["DEFAULT"]["key"])

    def get_nexus_cred(self) -> (str, str):
        return (self.config["NEXUS"]["nexus_user"],
                self.__fernet.decrypt(self.config["NEXUS"]["nexus_password"]).decode("utf-8"))

    def get_jenkins_cred(self) -> (str, str):
        return (self.config["JENKINS"]["jenkins_user"],
                self.__fernet.decrypt(self.config["JENKINS"]["jenkins_password"]).decode("utf-8"))

    def get_index_data_urls(self) -> list[str]:
        data = self.config["NEXUS"]["index_data_urls"]
        return [val.strip() for val in data.split(",")] if data is not None else []

    def get_smart_tests_all_url(self) -> str:
        return self.config["SMART_CLIENT"]["smart_tests_all"]

    def get_smart_tests_statistics_url(self) -> str:
        return self.config["SMART_CLIENT"]["smart_tests_statistics"]
