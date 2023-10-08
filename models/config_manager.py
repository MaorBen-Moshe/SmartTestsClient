from configparser import ConfigParser
from cryptography.fernet import Fernet
from decorators.singleton_decorator import singleton


@singleton
class ConfigManager:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")

    def get_nexus_cred(self) -> (str, str):
        return self.config["NEXUS"]["nexus_user"], self.config["NEXUS"]["nexus_password"]

    def get_jenkins_cred(self) -> (str, str):
        f = Fernet(self.config["DEFAULT"]["key"])
        return (self.config["JENKINS"]["jenkins_user"],
                f.decrypt(self.config["JENKINS"]["jenkins_password"]).decode("utf-8"))

    def get_helm_index_url(self) -> str:
        return self.config["NEXUS"]["helm_index_url"]
