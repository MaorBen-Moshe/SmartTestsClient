import base64
from configparser import ConfigParser

from cryptography.fernet import Fernet

from decorators.singleton_decorator import singleton


@singleton
class ConfigManager:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")

    def get_nexus_cred(self):
        return self.config["NEXUS"]["nexus_user"], self.config["NEXUS"]["nexus_password"]

    def get_jenkins_cred(self):
        f = Fernet(self.get_fernet_key())
        return self.config["JENKINS"]["jenkins_user"], f.decrypt(self.config["JENKINS"]["jenkins_password"])

    def get_helm_index_url(self):
        return self.config["NEXUS"]["helm_index_url"]

    def get_fernet_key(self):
        key = self.config["DEFAULT"]["key"]
        return base64.urlsafe_b64encode(key.encode("utf-8"))
