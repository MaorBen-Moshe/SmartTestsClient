from __future__ import annotations

from app.enums.res_info_level import ResInfoLevelEnum
from app.models.builder import Builder
from app.models.groups_data import TestGroupsData
from app.models.services_data import ServicesData
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.models.supported_group import SupportedGroup
from app.models.supported_groups import SupportedGroups


class AnalyzeAppServiceParameters:
    """A class that holds the parameters for analyzing an app service."""

    __slots__ = [
        "_build_url",
        "_group_name",
        "_supported_groups",
        "_session_id",
        "_smart_app_service_response",
        "_res_info_level",
        "_groups_data",
    ]

    def __init__(self):
        """Initialize the parameters with default values."""
        self._supported_groups: SupportedGroups = SupportedGroups()
        self.build_url: str | None = None
        self.group_name: str | None = None
        self.session_id: str | None = None
        self.smart_app_service_response: SmartAnalyzeResponse | None = None
        self.res_info_level: ResInfoLevelEnum | None = None
        self._groups_data: TestGroupsData = TestGroupsData()

    @property
    def services_map(self) -> ServicesData | None:
        """Get the services map for the current group data, or None if no group data."""
        if self.curr_group_data is None:
            return None

        return self.curr_group_data.services_data

    @property
    def groups_data(self) -> TestGroupsData:
        """Get the groups data."""
        return self._groups_data

    @property
    def build_url(self) -> str | None:
        """Get the build URL."""
        return self._build_url

    @build_url.setter
    def build_url(self, build_url: str | None) -> None:
        """Set the build URL."""
        self._build_url = build_url

    @property
    def group_name(self) -> str | None:
        """Get the group name."""
        return self._group_name

    @group_name.setter
    def group_name(self, group_name: str | None) -> None:
        """Set the group name."""
        self._group_name = group_name

    @property
    def supported_groups(self) -> SupportedGroups:
        """Get the supported groups."""
        return self._supported_groups

    @supported_groups.setter
    def supported_groups(self, supported_groups: SupportedGroups) -> None:
        """Set the supported groups."""
        self._supported_groups = supported_groups

    @property
    def session_id(self) -> str | None:
        """Get the session ID."""
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str | None) -> None:
        """Set the session ID."""
        self._session_id = session_id

    @property
    def smart_app_service_response(self) -> SmartAnalyzeResponse | None:
        """Get the smart app service response."""
        return self._smart_app_service_response

    @smart_app_service_response.setter
    def smart_app_service_response(self, smart_app_service_response: SmartAnalyzeResponse | None):
        """Set the smart app service response."""
        self._smart_app_service_response = smart_app_service_response

    @property
    def res_info_level(self) -> ResInfoLevelEnum:
        """Get the response info level."""
        return self._res_info_level

    @res_info_level.setter
    def res_info_level(self, res_info_level: ResInfoLevelEnum) -> None:
        """Set the response info level."""
        self._res_info_level = res_info_level

    @property
    def curr_group_data(self) -> SupportedGroup | None:
        """Get the current group data, or None if no group name."""
        return self.supported_groups.get_item(self.group_name)

    @staticmethod
    def create() -> AnalyzeAppServiceParametersBuilder:
        """Create a new instance of the class using a builder."""
        return AnalyzeAppServiceParametersBuilder()


class AnalyzeAppServiceParametersBuilder(Builder[AnalyzeAppServiceParameters]):
    """A builder class for creating AnalyzeAppServiceParameters instances."""

    def __init__(self, parameters=None):
        """Initialize the builder with an optional parameters instance."""
        parameters = parameters if parameters is not None else AnalyzeAppServiceParameters()
        super().__init__(parameters)

    def group_name(self, group_name: str | None) -> AnalyzeAppServiceParametersBuilder:
        """Set the group name and return the builder."""
        self._item.group_name = group_name
        return self

    def build_url(self, build_url: str | None) -> AnalyzeAppServiceParametersBuilder:
        """Set the build URL and return the builder."""
        self._item.build_url = build_url
        return self

    def supported_groups(self, supported_groups: SupportedGroups) -> AnalyzeAppServiceParametersBuilder:
        """Set the supported groups and return the builder."""
        self._item.supported_groups = supported_groups
        return self

    def session_id(self, session_id: str | None) -> AnalyzeAppServiceParametersBuilder:
        """Set the session ID and return the builder."""
        self._item.session_id = session_id
        return self

    def res_info_level(self, res_info_level: ResInfoLevelEnum) -> AnalyzeAppServiceParametersBuilder:
        """Set the response info level and return the builder."""
        self._item.res_info_level = res_info_level
        return self
