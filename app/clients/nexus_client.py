from __future__ import annotations

from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from app import config, app_main_logger
from app.constants.constants import NEXUS_REPOSITORY_KEY
from app.exceptions.excpetions import URLError


class NexusClient:
    def __init__(self):
        user, password = config.get_nexus_cred()
        self.user_cred = user
        self.password_cred = password
        self._url = config.get_nexus_search_url()

    def search_data(self, params: dict[str, str] | None) -> Any:
        if params is None or NEXUS_REPOSITORY_KEY not in params or params[NEXUS_REPOSITORY_KEY] is None:
            raise URLError("Provided to 'search_data' None repository query parameter.")

        app_main_logger.debug(f"NexusClient.search_data() params={params}")

        with requests.get(self._url,
                          auth=HTTPBasicAuth(self.user_cred, self.password_cred),
                          stream=True,
                          params=params) as response:
            response.raise_for_status()
            res_data = response.json()

        app_main_logger.debug(f"NexusClient.search_data() res_data={res_data}")

        return res_data
