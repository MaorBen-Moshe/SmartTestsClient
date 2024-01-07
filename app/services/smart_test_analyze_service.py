from __future__ import annotations

import concurrent.futures
import threading

from app import app_main_logger, executor_manager
from app.clients.smart_tests_client import SmartTestsClient
from app.constants.constants import SMART_SERVICE_GROUP_FLOWS_COUNT_KEY, SMART_SERVICE_GROUP_FLOWS_BY_GROUP_KEY, \
    SMART_SERVICE_GROUP_NAME_KEY, SMART_SERVICE_GROUP_TESTS_ALL_KEY, SMART_SERVICE_GROUP_FLOWS_KEY
from app.decorators.decorators import log_around
from app.exceptions.excpetions import EmptyInputError
from app.models.group_data import GroupData
from app.models.groups_data import TestGroupsData
from app.models.service_data import ServiceData
from app.models.services_data import ServicesData
from app.utils.utils import Utils


class SmartTestsAnalyzeService:
    """A class that analyzes the test flows of the microservices using the smart tests client."""

    def __init__(self):
        """Initializes the smart tests analyze service with a smart tests client and a lock."""
        self.client = SmartTestsClient()
        self._lock = threading.Lock()

    @log_around(print_output=False)
    def analyze_flows(self,
                      services_map: ServicesData | None,
                      filter_group: list[str] | None,
                      groups_data: TestGroupsData | None):
        """Analyzes the test flows of the microservices from the given services map and groups data.

        Args:
            services_map (ServicesData | None): The services map to analyze, or None to skip.
            filter_group (list[str] | None): The list of group names to filter the test flows by, or None to skip.
            groups_data (TestGroupsData | None): The groups data to update with the test flows, or None to skip.

        Raises:
            EmptyInputError: If the services map or the groups data is None or empty.
        """
        if services_map is not None and groups_data is not None:
            include_groups_filter = Utils.create_filter_by_list(filter_group)
            futures = []
            for service_key in services_map:
                service = services_map.get_item(service_key)
                if (service is None or
                        (service.pull_request_id is None and (services_map.get_item(service_key).to_version ==
                                                              services_map.get_item(service_key).from_version))):
                    continue

                f = executor_manager.submit(self._analyze_flow_per_service,
                                            service,
                                            groups_data,
                                            include_groups_filter)

                futures.append(f)

            concurrent.futures.wait(futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
        else:
            raise EmptyInputError("failed to fetch flows to analyze. no services or groups data found.")

    def _analyze_flow_per_service(self, service_data: ServiceData,
                                  groups_data: TestGroupsData,
                                  include_groups_filter: str):
        """Analyzes the test flows of a single microservice and updates its service data and group data.

        Args:
            service_data (ServiceData): The service data of the microservice to analyze.
            groups_data (TestGroupsData): The groups data to update with the test flows.
            include_groups_filter (str): The filter string to include only the relevant groups.
        """
        if service_data is None:
            return

        res_json = self.client.analyze_flows(service_data.repo_name,
                                             service_data.project,
                                             service_data.from_version,
                                             service_data.to_version,
                                             service_data.pull_request_id,
                                             include_groups_filter)

        if res_json is not None and int(res_json.get(SMART_SERVICE_GROUP_FLOWS_COUNT_KEY)) > 0:
            groups = res_json.get(SMART_SERVICE_GROUP_FLOWS_BY_GROUP_KEY)
            for group in groups:
                group_name = group.get(SMART_SERVICE_GROUP_NAME_KEY).split("/")[-1]
                if group_name in groups_data:
                    with self._lock:
                        groups_data.get_item(group_name).add_flows(group.get(SMART_SERVICE_GROUP_FLOWS_KEY))
                        service_data.add_flows(group.get(SMART_SERVICE_GROUP_FLOWS_KEY))
                else:
                    app_main_logger.warning(f"SmartTestsAnalyzeService._analyze_flow_per_service(): "
                                            f"Group {group_name} not found in groups data.")

    def get_all_flows_by_filter(self, include_filter_list: list[str] | None = None) -> TestGroupsData:
        """Gets all the test flows by the given filter list.

        Args:
            include_filter_list (list[str] | None): The list of group names to include in the test flows, or None to get all groups.

        Returns:
            TestGroupsData: The test groups data with the test flows that match the filter list.
        """
        app_main_logger.debug(f"SmartTestsAnalyzeService.get_all_flows_by_filter(): "
                              f"Get all flows by filter. include_filter_list={include_filter_list}")

        groups_data = TestGroupsData()
        include_filter_list = [] if include_filter_list is None else include_filter_list
        include_groups_filter = Utils.create_filter_by_list(include_filter_list)

        data = self.client.get_all_flows_stats(include_groups_filter)

        if (data is not None
                and type(data.get(SMART_SERVICE_GROUP_FLOWS_COUNT_KEY) is int)
                and data.get(SMART_SERVICE_GROUP_FLOWS_COUNT_KEY) > 0):
            for curr_xml in data.get(SMART_SERVICE_GROUP_TESTS_ALL_KEY):
                split_name = curr_xml.get(SMART_SERVICE_GROUP_NAME_KEY, "").rsplit('/', 1)
                if len(split_name) == 2:
                    path = split_name[0]
                    name = split_name[1]
                else:
                    name = split_name[0]
                    path = ""

                total_count = curr_xml.get(SMART_SERVICE_GROUP_FLOWS_COUNT_KEY)

                if len(include_filter_list) == 0 or name.replace(".xml", "") in include_filter_list:
                    groups_data.add_item(name, (GroupData
                                                .create()
                                                .test_xml_name(name)
                                                .test_xml_path(path)
                                                .total_flows_count(total_count)
                                                .build()))
        else:
            app_main_logger.warning(f"SmartTestsAnalyzeService.get_all_flows_by_filter(): "
                                    f"Failed to get all flows by filter. data={data}")

        app_main_logger.debug(f"SmartTestsAnalyzeService.get_all_flows_by_filter(): "
                              f"Get all flows by filter. groups_data={groups_data}")

        return groups_data
