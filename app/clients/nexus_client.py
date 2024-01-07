from __future__ import annotations

from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from app import config
from app.constants.constants import NEXUS_REPOSITORY_KEY
from app.decorators.decorators import gateway_errors_handler, log_around
from app.exceptions.excpetions import URLError


class NexusClient:
    """A class that interacts with the Nexus API."""

    def __init__(self):
        """Initializes the Nexus client with the credentials and the search URL."""
        user, password = config.get_nexus_cred()
        self.user_cred = user
        self.password_cred = password
        self._url = config.get_nexus_search_url()

    @gateway_errors_handler
    @log_around(print_output=True)
    def search_data(self, params: dict[str, str] | None) -> Any:
        """Searches for data in the Nexus repository using the given parameters.

        Args:
            params (dict[str, str] | None): A dictionary of query parameters, or None.

        Returns:
            Any: The JSON data returned by the Nexus API, or None if an error occurs.

        Raises:
            URLError: If the parameters are None or do not contain the NEXUS_REPOSITORY_KEY.
            BadGatewayError: If any other exception occurs while making the request or parsing the response.
        """
        if params is None or NEXUS_REPOSITORY_KEY not in params or params[NEXUS_REPOSITORY_KEY] is None:
            raise URLError("Provided to 'search_data' None repository query parameter.")

        with requests.get(self._url,
                          auth=HTTPBasicAuth(self.user_cred, self.password_cred),
                          stream=True,
                          params=params) as response:
            response.raise_for_status()
            res_data = response.json()

        return res_data
