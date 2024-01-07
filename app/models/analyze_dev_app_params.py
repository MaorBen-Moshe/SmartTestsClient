from __future__ import annotations

from app.enums.res_info_level import ResInfoLevelEnum
from app.models.builder import Builder
from app.models.groups_data import TestGroupsData
from app.models.services_data import ServicesData
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.models.supported_groups import SupportedGroups


class AnalyzeDevAppServiceParameters:
    """A class that holds the parameters for analyzing a dev app service."""

    __slots__ = [
        "_session_id",
        "_smart_app_service_response",
        "_res_info_level",
        "_services_map",
        "_groups_data",
        "_supported_groups",
    ]

    def __init__(self):
        """Initialize the parameters with default values."""
        self.smart_analyze_dev_app_service_response = None
        self.session_id: str | None = None
        self.res_info_level: ResInfoLevelEnum | None = None
        self._services_map: ServicesData | None = ServicesData()
        self._groups_data: TestGroupsData = TestGroupsData()
        self.supported_groups: SupportedGroups | None = None

    @property
    def services_map(self) -> ServicesData | None:
        """Get the services map."""
        return self._services_map

    @services_map.setter
    def services_map(self, services_map: ServicesData | None) -> None:
        """Set the services map."""
        self._services_map = services_map

    @property
    def groups_data(self) -> TestGroupsData:
        """Get the groups data."""
        return self._groups_data

    @property
    def session_id(self) -> str | None:
        """Get the session id."""
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str | None) -> None:
        """Set the session id."""
        self._session_id = session_id

    @property
    def smart_analyze_dev_app_service_response(self) -> SmartAnalyzeResponse | None:
        """Get the smart analyze dev app service response."""
        return self._smart_app_service_response

    @smart_analyze_dev_app_service_response.setter
    def smart_analyze_dev_app_service_response(self, smart_app_service_response: SmartAnalyzeResponse | None):
        """Set the smart analyze dev app service response."""
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
    def supported_groups(self) -> SupportedGroups | None:
        """Get the supported groups."""
        return self._supported_groups

    @supported_groups.setter
    def supported_groups(self, supported_groups: SupportedGroups | None) -> None:
        """Set the supported groups."""
        self._supported_groups = supported_groups

    @staticmethod
    def create():
        """Create a new instance of the class using a builder."""
        return AnalyzeDevAppServiceParametersBuilder()


class AnalyzeDevAppServiceParametersBuilder(Builder[AnalyzeDevAppServiceParameters]):
    """A builder class for creating AnalyzeDevAppServiceParameters instances."""

    def __init__(self, parameters=None):
        """Initialize the builder with an optional parameters instance."""
        parameters = parameters if parameters else AnalyzeDevAppServiceParameters()
        super().__init__(parameters)

    def services_map(self, services_map: ServicesData) -> AnalyzeDevAppServiceParametersBuilder:
        """Set the services map and return the builder."""
        self._item.services_map = services_map
        return self

    def session_id(self, session_id: str | None) -> AnalyzeDevAppServiceParametersBuilder:
        """Set the session id and return the builder."""
        self._item.session_id = session_id
        return self

    def res_info_level(self, res_info_level: ResInfoLevelEnum) -> AnalyzeDevAppServiceParametersBuilder:
        """Set the response info level and return the builder."""
        self._item.res_info_level = res_info_level
        return self

    def supported_groups(self, supported_groups: SupportedGroups | None) -> AnalyzeDevAppServiceParametersBuilder:
        """Set the supported groups and return the builder."""
        self._item.supported_groups = supported_groups
        return self
