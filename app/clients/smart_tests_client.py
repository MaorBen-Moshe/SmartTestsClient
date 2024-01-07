from __future__ import annotations

import requests

from app import config, cache_manager
from app.decorators.decorators import gateway_errors_handler, log_around
from app.utils.utils import Utils


class SmartTestsClient:
    """A class that interacts with the Smart Tests API."""

    def __init__(self):
        """Initializes the Smart Tests client with the URLs for the API endpoints."""
        self.smart_tests_all_url = config.get_smart_tests_all_url()
        self.smart_tests_statistics_url = config.get_smart_tests_statistics_url()

    @gateway_errors_handler
    @log_around(print_output=True)
    @cache_manager.cached(timeout=config.get_smart_analyze_endpoint_cache_ttl(),
                          make_cache_key=Utils.make_cache_key_smart_analyze_flows,
                          unless=lambda: not config.is_smart_analyze_endpoint_cache_enabled())
    def analyze_flows(self,
                      repo_name: str | None,
                      project: str | None,
                      from_version: str | None,
                      to_version: str | None,
                      pull_request_id: str | None,
                      include_groups_filter: str | None):
        """Analyzes the flows for a given repository, project, and version range.

        Args:
            repo_name (str | None): The name of the repository, or None.
            project (str | None): The name of the project, or None.
            from_version (str | None): The starting version, or None.
            to_version (str | None): The ending version, or None.
            pull_request_id (str | None): The pull request ID, or None.
            include_groups_filter (str | None): The filter for the file group names, or None.

        Returns:
            Any: The JSON data returned by the Smart Tests API, or None if an error occurs or the arguments are invalid.

        Raises:
            BadGatewayError: If any exception occurs while making the request or parsing the response.
        """
        if repo_name is None or project is None:
            return None

        if include_groups_filter is None:
            include_groups_filter = ""

        body = [
            {
                "infoLevel": "info",
                "restrictions": [
                    "repo_exclude_config"
                ],
                "project": project,
                "repo": repo_name,
                "from": from_version,
                "to": to_version,
                "pullRequestId": pull_request_id,
                "includeFileGroupNamePattern": include_groups_filter
            }
        ]

        with requests.post(
                url=self.smart_tests_statistics_url,
                params={"queryType": "repo"},
                json=body,
                verify=False) as res:
            res.raise_for_status()
            res_json = res.json()

        return res_json

    @gateway_errors_handler
    @log_around(print_output=True)
    @cache_manager.cached(timeout=config.get_get_all_endpoint_cache_ttl(),
                          make_cache_key=Utils.make_cache_key_smart_get_all,
                          unless=lambda: not config.is_get_all_endpoint_cache_enabled())
    def get_all_flows_stats(self, include_groups_filter: str | None):
        """Gets the statistics for all the flows in the Smart Tests database.

        Args:
            include_groups_filter (str | None): The filter for the file group names, or None.

        Returns:
            Any: The JSON data returned by the Smart Tests API, or None if an error occurs.

        Raises:
            BadGatewayError: If any exception occurs while making the request or parsing the response.
        """
        body = []
        if include_groups_filter:
            body.append({
                "includeFileGroupNamePattern": include_groups_filter
            })

        with requests.post(url=self.smart_tests_all_url,
                           json=body,
                           verify=False) as res:
            res.raise_for_status()
            data = res.json()

        return data
