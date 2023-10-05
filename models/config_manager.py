from configparser import ConfigParser

from decorators.singleton_decorator import singleton


@singleton
class ConfigManager:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")

    def get_nexus_cred(self):
        return self.config["NEXUS"]["nexus_user"], self.config["NEXUS"]["nexus_password"]

    def get_jenkins_cred(self):
        return self.config["JENKINS"]["jenkins_user"], self.config["JENKINS"]["jenkins_password"]

    def get_helm_index_url(self):
        return self.config["NEXUS"]["helm_index_url"]
