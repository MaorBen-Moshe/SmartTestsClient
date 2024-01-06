from __future__ import annotations

from app.models.builder import Builder
from app.models.services_data import ServicesData


class SupportedGroup:

    __slots__ = [
        "_group_name",
        "_cluster",
        "_test_files",
        "_url",
        "_services_data",
        "_project",
    ]

    def __init__(self):
        self.group_name: str | None = None
        self.cluster: str | None = None
        self.test_files: list[str] = []
        self.url: str | None = None
        self.services_data: ServicesData = ServicesData()
        self.project: str | None = None

    @property
    def group_name(self) -> str | None:
        return self._group_name

    @group_name.setter
    def group_name(self, group_name: str | None):
        self._group_name = group_name

    @property
    def cluster(self) -> str | None:
        return self._cluster

    @cluster.setter
    def cluster(self, cluster: str | None):
        self._cluster = cluster

    @property
    def url(self) -> str | None:
        return self._url

    @url.setter
    def url(self, url: str | None):
        self._url = url

    @property
    def test_files(self) -> list[str]:
        return self._test_files

    @test_files.setter
    def test_files(self, test_files: list[str]):
        self._test_files = test_files

    @property
    def services_data(self) -> ServicesData:
        return self._services_data

    @services_data.setter
    def services_data(self, services_data: ServicesData):
        self._services_data = services_data

    @property
    def project(self) -> str | None:
        return self._project

    @project.setter
    def project(self, project: str | None):
        self._project = project

    @staticmethod
    def create():
        return SupportedGroupBuilder()


class SupportedGroupBuilder(Builder[SupportedGroup]):
    def __init__(self, supported_group=None):
        supported_group = supported_group if supported_group is not None else SupportedGroup()
        super().__init__(supported_group)

    def group_name(self, group_name: str | None) -> SupportedGroupBuilder:
        self._item.group_name = group_name
        return self

    def cluster(self, cluster: str | None) -> SupportedGroupBuilder:
        self._item.cluster = cluster
        return self

    def url(self, url: str | None) -> SupportedGroupBuilder:
        self._item.url = url
        return self

    def test_files(self, test_files: list[str]) -> SupportedGroupBuilder:
        self._item.test_files = test_files
        return self

    def services_data(self, services_data: ServicesData) -> SupportedGroupBuilder:
        self._item.services_data = services_data
        return self

    def project(self, project: str | None) -> SupportedGroupBuilder:
        self._item.project = project
        return self
