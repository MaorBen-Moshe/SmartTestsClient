from __future__ import annotations

from typing import Any

from app.enums.res_info_level import ResInfoLevelEnum
from app.models.builder import Builder
from app.models.groups_data import TestGroupsData
from app.models.services_data import ServicesData
from app.models.smart_analyze_response import SmartAnalyzeResponse


class AnalyzeDevAppServiceParameters:
    def __init__(self):
        self.smart_analyze_dev_app_service_response = None
        self.services_input = None
        self.session_id: str | None = None
        self.res_info_level: ResInfoLevelEnum | None = None
        self._services_map: ServicesData = ServicesData()
        self._groups_data: TestGroupsData = TestGroupsData()

    @property
    def services_input(self) -> Any:
        return self._services_input

    @services_input.setter
    def services_input(self, services_input: Any) -> None:
        self._services_input = services_input

    @property
    def services_map(self) -> ServicesData | None:
        return self._services_map

    @property
    def groups_data(self) -> TestGroupsData:
        return self._groups_data

    @property
    def session_id(self) -> str | None:
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str | None) -> None:
        self._session_id = session_id

    @property
    def smart_analyze_dev_app_service_response(self) -> SmartAnalyzeResponse | None:
        return self._smart_app_service_response

    @smart_analyze_dev_app_service_response.setter
    def smart_analyze_dev_app_service_response(self, smart_app_service_response: SmartAnalyzeResponse | None):
        self._smart_app_service_response = smart_app_service_response

    @property
    def res_info_level(self) -> ResInfoLevelEnum:
        return self._res_info_level

    @res_info_level.setter
    def res_info_level(self, res_info_level: ResInfoLevelEnum) -> None:
        self._res_info_level = res_info_level

    @staticmethod
    def create():
        return AnalyzeDevAppServiceParametersBuilder()


class AnalyzeDevAppServiceParametersBuilder(Builder[AnalyzeDevAppServiceParameters]):
    def __init__(self, parameters=None):
        parameters = parameters if parameters else AnalyzeDevAppServiceParameters()
        super().__init__(parameters)

    def services_input(self, services_input: Any) -> AnalyzeDevAppServiceParametersBuilder:
        self.item.services_input = services_input
        return self

    def session_id(self, session_id: str | None) -> AnalyzeDevAppServiceParametersBuilder:
        self.item.session_id = session_id
        return self

    def res_info_level(self, res_info_level: ResInfoLevelEnum) -> AnalyzeDevAppServiceParametersBuilder:
        self.item.res_info_level = res_info_level
        return self
