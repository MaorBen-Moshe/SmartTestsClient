from __future__ import annotations

from app.models.builder import Builder
from app.models.dto.group_data_dto import GroupDataDTO
from app.models.dto.service_data_dto import ServiceDataDTO
from app.models.serializable_model import Serializable


class SmartAnalyzeResponse(Serializable):
    """A class that represents the smart analyze response with the test flows and the services data."""

    __slots__ = [
        "_total_flows_count",
        "_curr_flows_count",
        "_groups",
        "_services",
    ]

    def __init__(self):
        """Initializes the smart analyze response with zero values for the counts and empty values for the groups and
        the services."""
        self.total_flows_count = 0
        self.curr_flows_count = 0
        self.groups: dict[str, GroupDataDTO] = {}
        self.services: list[ServiceDataDTO] | None = []

    @property
    def total_flows_count(self) -> int:
        """Gets or sets the total number of test flows in the response.

        Returns:
            int: The total number of test flows in the response.
        """
        return self._total_flows_count

    @total_flows_count.setter
    def total_flows_count(self, total_flows_count: int):
        """Sets the total number of test flows in the response.

        Args:
            total_flows_count (int): The total number of test flows in the response.
        """
        self._total_flows_count = total_flows_count

    @property
    def curr_flows_count(self) -> int:
        """Gets or sets the current number of test flows in the response.

        Returns:
            int: The current number of test flows in the response.
        """
        return self._curr_flows_count

    @curr_flows_count.setter
    def curr_flows_count(self, curr_flows_count: int):
        """Sets the current number of test flows in the response.

        Args:
            curr_flows_count (int): The current number of test flows in the response.
        """
        self._curr_flows_count = curr_flows_count

    @property
    def groups(self) -> dict[str, GroupDataDTO] | None:
        """Gets or sets the dictionary of test groups in the response.

        Returns:
            dict[str, GroupDataDTO] | None: The dictionary of test groups in the response, or None if not set.
        """
        return self._groups

    @groups.setter
    def groups(self, groups: dict[str, GroupDataDTO] | None):
        """Sets the dictionary of test groups in the response.

        Args:
            groups (dict[str, GroupDataDTO] | None): The dictionary of test groups in the response, or None to unset it.
        """
        self._groups = groups

    @property
    def services(self) -> list[ServiceDataDTO] | None:
        """Gets or sets the list of services data in the response.

        Returns:
            list[ServiceDataDTO] | None: The list of services data in the response, or None if not set.
        """
        return self._services

    @services.setter
    def services(self, services: list[ServiceDataDTO] | None):
        """Sets the list of services data in the response.

        Args:
            services (list[ServiceDataDTO] | None): The list of services data in the response, or None to unset it.
        """
        self._services = services

    @staticmethod
    def create():
        """Creates a new smart analyze response builder.

        Returns:
            SmartAnalyzeResponseBuilder: A smart analyze response builder instance.
        """
        return SmartAnalyzeResponseBuilder()


class SmartAnalyzeResponseBuilder(Builder[SmartAnalyzeResponse]):
    """A class that builds a smart analyze response instance."""

    def __init__(self, smart_analyze_response=None):
        """Initializes the smart analyze response builder with a smart analyze response instance.

        Args:
            smart_analyze_response (SmartAnalyzeResponse | None): The smart analyze response instance to build, or None to create a new one.
        """
        smart_analyze_response = smart_analyze_response if smart_analyze_response is not None \
                                                        else SmartAnalyzeResponse()
        super().__init__(smart_analyze_response)

    def total_flows_count(self, total_flows_count: int) -> SmartAnalyzeResponseBuilder:
        """Sets the total number of test flows for the smart analyze response to build.

        Args:
            total_flows_count (int): The total number of test flows for the smart analyze response to build.

        Returns:
            SmartAnalyzeResponseBuilder: The same smart analyze response builder instance, for method chaining.
        """
        self._item.total_flows_count = total_flows_count
        return self

    def curr_flows_count(self, curr_flows_count: int) -> SmartAnalyzeResponseBuilder:
        """Sets the current number of test flows for the smart analyze response to build.

        Args:
            curr_flows_count (int): The current number of test flows for the smart analyze response to build.

        Returns:
            SmartAnalyzeResponseBuilder: The same smart analyze response builder instance, for method chaining.
        """
        self._item.curr_flows_count = curr_flows_count
        return self

    def groups(self, groups: dict[str, GroupDataDTO] | None) -> SmartAnalyzeResponseBuilder:
        """Sets the dictionary of test groups for the smart analyze response to build.

        Args:
            groups (dict[str, GroupDataDTO] | None): The dictionary of test groups for the smart analyze response to build, or None to unset it.

        Returns:
            SmartAnalyzeResponseBuilder: The same smart analyze response builder instance, for method chaining.
        """
        self._item.groups = groups
        return self

    def services(self, services: list[ServiceDataDTO] | None) -> SmartAnalyzeResponseBuilder:
        """Sets the list of services data for the smart analyze response to build.

        Args:
            services (list[ServiceDataDTO] | None): The list of services data for the smart analyze response to build, or None to unset it.

        Returns:
            SmartAnalyzeResponseBuilder: The same smart analyze response builder instance, for method chaining.
        """
        self._item.services = services
        return self
