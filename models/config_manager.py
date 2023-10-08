from configparser import ConfigParser
from cryptography.fernet import Fernet
from decorators.singleton_decorator import singleton


@singleton
class ConfigManager:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.__fernet = Fernet(self.config["DEFAULT"]["key"])

    def get_nexus_cred(self) -> (str, str):

        return (self.config["NEXUS"]["nexus_user"],
                self.__fernet.decrypt(self.config["NEXUS"]["nexus_password"]).decode("utf-8"))

    def get_jenkins_cred(self) -> (str, str):
        return (self.config["JENKINS"]["jenkins_user"],
                self.__fernet.decrypt(self.config["JENKINS"]["jenkins_password"]).decode("utf-8"))

    def get_helm_index_url(self) -> str:
        return self.config["NEXUS"]["helm_index_url"]
