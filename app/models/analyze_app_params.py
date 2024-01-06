from __future__ import annotations

from app.enums.res_info_level import ResInfoLevelEnum
from app.models.builder import Builder
from app.models.groups_data import TestGroupsData
from app.models.services_data import ServicesData
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.models.supported_group import SupportedGroup
from app.models.supported_groups import SupportedGroups


class AnalyzeAppServiceParameters:
    def __init__(self):
        self._supported_groups: SupportedGroups = SupportedGroups()
        self.build_url: str | None = None
        self.group_name: str | None = None
        self.session_id: str | None = None
        self.smart_app_service_response: SmartAnalyzeResponse | None = None
        self.res_info_level: ResInfoLevelEnum | None = None
        self._groups_data: TestGroupsData = TestGroupsData()

    @property
    def services_map(self) -> ServicesData | None:
        if self.curr_group_data is None:
            return None

        return self.curr_group_data.services_data

    @property
    def groups_data(self) -> TestGroupsData:
        return self._groups_data

    @property
    def build_url(self) -> str | None:
        return self._build_url

    @build_url.setter
    def build_url(self, build_url: str | None) -> None:
        self._build_url = build_url

    @property
    def group_name(self) -> str | None:
        return self._group_name

    @group_name.setter
    def group_name(self, group_name: str | None) -> None:
        self._group_name = group_name

    @property
    def supported_groups(self) -> SupportedGroups:
        return self._supported_groups

    @supported_groups.setter
    def supported_groups(self, supported_groups: SupportedGroups) -> None:
        self._supported_groups = supported_groups

    @property
    def session_id(self) -> str | None:
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str | None) -> None:
        self._session_id = session_id

    @property
    def smart_app_service_response(self) -> SmartAnalyzeResponse | None:
        return self._smart_app_service_response

    @smart_app_service_response.setter
    def smart_app_service_response(self, smart_app_service_response: SmartAnalyzeResponse | None):
        self._smart_app_service_response = smart_app_service_response

    @property
    def res_info_level(self) -> ResInfoLevelEnum:
        return self._res_info_level

    @res_info_level.setter
    def res_info_level(self, res_info_level: ResInfoLevelEnum) -> None:
        self._res_info_level = res_info_level

    @property
    def curr_group_data(self) -> SupportedGroup | None:
        return self.supported_groups.get_item(self.group_name)

    @staticmethod
    def create() -> AnalyzeAppServiceParametersBuilder:
        return AnalyzeAppServiceParametersBuilder()


class AnalyzeAppServiceParametersBuilder(Builder[AnalyzeAppServiceParameters]):
    def __init__(self, parameters=None):
        parameters = parameters if parameters is not None else AnalyzeAppServiceParameters()
        super().__init__(parameters)

    def group_name(self, group_name: str | None) -> AnalyzeAppServiceParametersBuilder:
        self._item.group_name = group_name
        return self

    def build_url(self, build_url: str | None) -> AnalyzeAppServiceParametersBuilder:
        self._item.build_url = build_url
        return self

    def supported_groups(self, supported_groups: SupportedGroups) -> AnalyzeAppServiceParametersBuilder:
        self._item.supported_groups = supported_groups
        return self

    def session_id(self, session_id: str | None) -> AnalyzeAppServiceParametersBuilder:
        self._item.session_id = session_id
        return self

    def res_info_level(self, res_info_level: ResInfoLevelEnum) -> AnalyzeAppServiceParametersBuilder:
        self._item.res_info_level = res_info_level
        return self
