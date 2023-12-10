from __future__ import annotations

from typing import Any

from app.models.builder import Builder
from app.models.data_manager import DataManager
from app.models.service_data import ServiceData
from app.models.smart_analyze_response import SmartAnalyzeResponse


class AnalyzeDevAppServiceParameters:
    def __init__(self):
        self.smart_analyze_dev_app_service_response = None
        self.services_input = None
        self.__data_manager = DataManager()
        self.session_id: str | None = None

    @property
    def services_input(self) -> Any:
        return self._services_input

    @services_input.setter
    def services_input(self, services_input: Any) -> None:
        self._services_input = services_input

    @property
    def data_manager(self) -> DataManager:
        return self.__data_manager

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

    def services(self, services: dict[str, ServiceData]) -> AnalyzeDevAppServiceParametersBuilder:
        self.item.services = services
        return self

    def session_id(self, session_id: str | None) -> AnalyzeDevAppServiceParametersBuilder:
        self.item.session_id = session_id
        return self
