from __future__ import annotations

from app.models.serializable_model import Serializable


class SupportedGroupDTO(Serializable):
    def __init__(self):
        self.group_name: str | None = None
        self.cluster: str | None = None
        self.test_files: list[str] = []
        self.url: str | None = None
        self.ms_list: list[str] = []
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
    def ms_list(self) -> list[str]:
        return self._ms_list

    @ms_list.setter
    def ms_list(self, ms_list: list[str]):
        self._ms_list = ms_list

    @property
    def project(self) -> str | None:
        return self._project

    @project.setter
    def project(self, project: str | None):
        self._project = project
