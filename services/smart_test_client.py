import requests

from constants.constants import MS_POSTFIX
from exceptions.excpetions import EmptyInputError
from models.group_data import GroupData, GroupDataBuilder
from models.service_data import ServiceData


class SmartTestsClient:

    def analyze_flows(self,
                      services_map: dict[str, ServiceData],
                      filter_group: list[str],
                      groups_data: dict[str, GroupData]):
        if services_map is not None:
            for service_key in services_map:
                if services_map[service_key].old_version == services_map[service_key].new_version:
                    continue

                body = [
                    {
                        "infoLevel": "info",
                        "restrictions": [
                            "repo_exclude_config"
                        ],
                        "project": "DIGOC",
                        "repo": f"{service_key}{MS_POSTFIX}",
                        "to": services_map.get(service_key).old_version,
                        "from": services_map.get(service_key).new_version,
                        "includeFileGroupNamePattern": self.__create_filter_by_list(filter_group)
                    }
                ]

                with requests.post(
                        url="https://amd-apigw-stack-service-oc-cd-ml-devops-light-tracer.apps.ilocpde529.ocpd.corp"
                            ".amdocs.com/lightTracer/v1/smart-tests-statistics",
                        params={"queryType": "repo"},
                        json=body,
                        verify=False) as res:
                    res.raise_for_status()
                    res_json = res.json()

                if int(res_json.get("flowsCount")) > 0:
                    groups = res_json.get("flowsByGroupName")
                    for group in groups:
                        group_name = group.get("name").split("/")[-1]
                        if group_name in groups_data:
                            groups_data.get(group_name).add_flows(group.get("flows"))
        else:
            raise EmptyInputError("failed to fetch flows to analyze. no services found.")

    def get_all_flows_by_filter(self, include_filter_list: list) -> dict[str, GroupData]:
        groups_data = {}
        body = []
        include_filter = self.__create_filter_by_list(include_filter_list)
        if include_filter:
            body.append({
                "includeFileGroupNamePattern": include_filter
            })

        with requests.post(url="https://amd-apigw-stack-service-oc-cd-ml-devops-light-tracer.apps.ilocpde529.ocpd.corp"
                               ".amdocs.com/lightTracer/v1/smart-tests-all",
                           json=body,
                           verify=False) as res:
            res.raise_for_status()
            data = res.json()

        for curr_xml in data.get("smartTestsAllItem"):
            split_name = curr_xml.get("name").rsplit('/', 1)
            if len(split_name) == 2:
                path = split_name[0]
                name = split_name[1]

                total_count = curr_xml.get("flowsCount")

                if name.replace(".xml", "") in include_filter_list:
                    groups_data[name] = (GroupDataBuilder()
                                         .group_name(name)
                                         .group_path(path)
                                         .total_flows_count(total_count)
                                         .build())

        return groups_data

    def __create_filter_by_list(self, values: list) -> str:
        if values is None or len(values) == 0:
            return ""

        values = [f".*{value}.*" for value in values]
        return "|".join(values)
