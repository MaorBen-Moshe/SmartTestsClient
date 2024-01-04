from __future__ import annotations

import requests

from app import config, cache_manager
from app.decorators.decorators import gateway_errors_handler, log_around
from app.models.service_data import ServiceData
from app.utils.utils import Utils


class SmartTestsClient:
    def __init__(self):
        self.smart_tests_all_url = config.get_smart_tests_all_url()
        self.smart_tests_statistics_url = config.get_smart_tests_statistics_url()

    @gateway_errors_handler
    @log_around(print_output=True)
    def analyze_flows(self,
                      service_key: str | None,
                      service_data: ServiceData | None,
                      include_groups_filter: str | None):

        if service_key is None or service_data is None:
            return None

        if include_groups_filter is None:
            include_groups_filter = ""

        body = [
            {
                "infoLevel": "info",
                "restrictions": [
                    "repo_exclude_config"
                ],
                "project": service_data.project,
                "repo": service_data.repo_name,
                "from": service_data.from_version,
                "to": service_data.to_version,
                "pullRequestId": service_data.pull_request_id,
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
    @cache_manager.cached(timeout=600,
                          make_cache_key=Utils.make_cache_key_smart_get_all,
                          unless=lambda: not config.is_get_all_endpoint_cache_enabled())
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
