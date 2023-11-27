from __future__ import annotations

from app.models.builder import Builder
from app.models.supported_group import SupportedGroup


class AnalyzeAppServiceParameters:
    def __init__(self):
        self._supported_groups: dict[str, SupportedGroup] = {}
        self._filtered_ms_list: list[str] = []
        self.build_url: str | None = None
        self.group_name: str | None = None
        self.session_id: str | None = None

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
    def supported_groups(self) -> dict[str, SupportedGroup]:
        return self._supported_groups

    @supported_groups.setter
    def supported_groups(self, supported_groups: dict[str, SupportedGroup]) -> None:
        self._supported_groups = supported_groups

    @property
    def filtered_ms_list(self) -> list[str]:
        return self._filtered_ms_list

    @filtered_ms_list.setter
    def filtered_ms_list(self, filtered_ms_list: list[str]) -> None:
        self._filtered_ms_list = filtered_ms_list

    @property
    def session_id(self) -> str | None:
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str | None) -> None:
        self._session_id = session_id

    @staticmethod
    def create():
        return AnalyzeAppServiceParametersBuilder()


class AnalyzeAppServiceParametersBuilder(Builder[AnalyzeAppServiceParameters]):
    def __init__(self, parameters=None):
        parameters = parameters if parameters is not None else AnalyzeAppServiceParameters()
        super().__init__(parameters)

    def group_name(self, group_name: str | None) -> AnalyzeAppServiceParametersBuilder:
        self.item.group_name = group_name
        return self

    def build_url(self, build_url: str | None) -> AnalyzeAppServiceParametersBuilder:
        self.item.build_url = build_url
        return self

    def supported_groups(self, supported_groups: dict[str, SupportedGroup]) -> AnalyzeAppServiceParametersBuilder:
        self.item.supported_groups = supported_groups
        return self

    def filtered_ms_list(self, filtered_ms_list: list[str]) -> AnalyzeAppServiceParametersBuilder:
        self.item.filtered_ms_list = filtered_ms_list
        return self

    def session_id(self, session_id: str | None) -> AnalyzeAppServiceParametersBuilder:
        self.item.session_id = session_id
        return self
