from __future__ import annotations

import requests

from constants.constants import MS_POSTFIX
from models.config_manager import ConfigManager


class SmartTestsClient:
    def __init__(self):
        config = ConfigManager()
        self.smart_tests_all_url = config.get_smart_tests_all_url()
        self.smart_tests_statistics_url = config.get_smart_tests_statistics_url()

    def analyze_flows(self,
                      service_key: str | None,
                      old_version: str | None,
                      new_version: str | None,
                      include_groups_filter: str | None):

        if include_groups_filter is None:
            include_groups_filter = ""

        body = [
            {
                "infoLevel": "info",
                "restrictions": [
                    "repo_exclude_config"
                ],
                "project": "DIGOC",
                "repo": f"{service_key}{MS_POSTFIX}",
                "to": old_version,
                "from": new_version,
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

    def get_all_flows_stats(self, include_groups_filter: str | None):
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
