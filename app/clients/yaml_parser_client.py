from __future__ import annotations

import requests
import yaml
from requests.auth import HTTPBasicAuth

from app.exceptions.excpetions import URLError
from app.models.config_manager import ConfigManager
from app.utils.utils import Utils


class YamlParserClient:
    def __init__(self):
        config = ConfigManager()
        user, password = config.get_nexus_cred()
        self.user_cred = user
        self.password_cred = password

    def get_yaml(self, yaml_url: str | None):
        if not Utils.is_valid_url(yaml_url):
            raise URLError(f"Yaml url: '{yaml_url}' is not valid.")

        with requests.get(yaml_url,
                          auth=HTTPBasicAuth(self.user_cred, self.password_cred),
                          stream=True) as response:
            response.raise_for_status()
            res_data = response.content

        try:
            data = yaml.safe_load(res_data)
        except:
            return None
        else:
            return data
