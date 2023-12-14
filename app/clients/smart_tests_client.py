from __future__ import annotations

import requests

from app import config, app_main_logger
from app.constants.constants import MS_POSTFIX
from app.models.service_data import ServiceData


class SmartTestsClient:
    def __init__(self):
        self.smart_tests_all_url = config.get_smart_tests_all_url()
        self.smart_tests_statistics_url = config.get_smart_tests_statistics_url()

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
                "repo": f"{service_key}{MS_POSTFIX}",
                "from": service_data.from_version,
                "to": service_data.to_version,
                "pullRequestId": service_data.pull_request_id,
                "includeFileGroupNamePattern": include_groups_filter
            }
        ]

        app_main_logger.debug(f"SmartTestsClient.analyze_flows(): Analyze flows. body={body}")

        with requests.post(
                url=self.smart_tests_statistics_url,
                params={"queryType": "repo"},
                json=body,
                verify=False) as res:
            res.raise_for_status()
            res_json = res.json()

        app_main_logger.debug(f"SmartTestsClient.analyze_flows(): Analyze flows. res_json={res_json}")

        return res_json

    def get_all_flows_stats(self, include_groups_filter: str | None):
        body = []
        if include_groups_filter:
            body.append({
                "includeFileGroupNamePattern": include_groups_filter
            })

        app_main_logger.debug(f"SmartTestsClient.get_all_flows_stats(): Get all flows stats. body={body}")

        with requests.post(url=self.smart_tests_all_url,
                           json=body,
                           verify=False) as res:
            res.raise_for_status()
            data = res.json()

        app_main_logger.debug(f"SmartTestsClient.get_all_flows_stats(): Get all flows stats. data={data}")

        return data
