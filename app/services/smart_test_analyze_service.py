from __future__ import annotations

from app.clients.smart_tests_client import SmartTestsClient
from app.exceptions.excpetions import EmptyInputError
from app.models.group_data import GroupData
from app.models.service_data import ServiceData
from app.utils.utils import Utils


class SmartTestsAnalyzeService:

    def __init__(self):
        self.client = SmartTestsClient()

    def analyze_flows(self,
                      services_map: dict[str, ServiceData] | None,
                      filter_group: list[str] | None,
                      groups_data: dict[str, GroupData] | None):
        if services_map is not None and groups_data is not None:
            include_groups_filter = Utils.create_filter_by_list(filter_group)
            for service_key in services_map:
                if services_map[service_key].old_version == services_map[service_key].new_version:
                    continue

                res_json = self.client.analyze_flows(service_key,
                                                     services_map.get(service_key).old_version,
                                                     services_map.get(service_key).new_version,
                                                     include_groups_filter)

                if res_json is not None and int(res_json.get("flowsCount")) > 0:
                    groups = res_json.get("flowsByGroupName")
                    for group in groups:
                        group_name = group.get("name").split("/")[-1]
                        if group_name in groups_data:
                            groups_data.get(group_name).add_flows(group.get("flows"))
        else:
            raise EmptyInputError("failed to fetch flows to analyze. no services or groups data found.")

    def get_all_flows_by_filter(self, include_filter_list: list[str] | None) -> dict[str, GroupData]:
        groups_data = {}
        include_groups_filter = Utils.create_filter_by_list(include_filter_list)

        data = self.client.get_all_flows_stats(include_groups_filter)

        if data is not None and type(data.get("flowsCount") is int) and data.get("flowsCount") > 0:
            for curr_xml in data.get("smartTestsAllItem"):
                split_name = curr_xml.get("name", "").rsplit('/', 1)
                if len(split_name) == 2:
                    path = split_name[0]
                    name = split_name[1]
                else:
                    name = split_name[0]
                    path = ""

                total_count = curr_xml.get("flowsCount")

                if len(include_filter_list) == 0 or name.replace(".xml", "") in include_filter_list:
                    groups_data[name] = (GroupData
                                         .create()
                                         .test_xml_name(name)
                                         .test_xml_path(path)
                                         .total_flows_count(total_count)
                                         .build())

        return groups_data