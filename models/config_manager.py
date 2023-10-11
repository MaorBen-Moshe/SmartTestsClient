from configparser import ConfigParser
from cryptography.fernet import Fernet
from models.singleton_meta import SingletonMeta


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        self.__fernet = None
        self.config = ConfigParser()

    def init_configs(self, config_path: str):
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
        urls = []
        if data is None:
            return urls
        else:
            urls.extend([val.strip() for val in data.split(",")])
