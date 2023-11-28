from __future__ import annotations

from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from app import config
from app.exceptions.excpetions import URLError


class NexusClient:
    def __init__(self):
        user, password = config.get_nexus_cred()
        self.user_cred = user
        self.password_cred = password
        self._url = "http://illin5589:28080/service/rest/v1/search"

    def search_data(self, params: dict[str, str] | None) -> Any:
        if params is None or 'repository' not in params or params['repository'] is None:
            raise URLError("Provided to 'search_data' None repository query parameter.")

        with requests.get(self._url,
                          auth=HTTPBasicAuth(self.user_cred, self.password_cred),
                          stream=True,
                          params=params) as response:
            response.raise_for_status()
            res_data = response.json()

        return res_data
