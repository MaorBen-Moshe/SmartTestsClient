from __future__ import annotations

from app.models.serializable_model import Serializable
from app.models.service_data import ServiceData


class SupportedGroupDTO(Serializable):
    """A data transfer object that represents a supported group of microservices."""

    __slots__ = [
        "_namespace",
        "_cluster",
        "_test_files",
        "_url",
        "_ms_list",
        "_project",
    ]

    def __init__(self):
        """Initialize the attributes of the supported group."""
        self.namespace: str | None = None
        self.cluster: str | None = None
        self.test_files: list[str] = []
        self.url: str | None = None
        self.ms_list: list[ServiceData] = []
        self.project: str | None = None

    @property
    def namespace(self) -> str | None:
        """Get the namespace of the supported group."""
        return self._namespace

    @namespace.setter
    def namespace(self, namespace: str | None):
        """Set the namespace of the supported group."""
        self._namespace = namespace

    @property
    def cluster(self) -> str | None:
        """Get the name of the cluster where the supported group is deployed."""
        return self._cluster

    @cluster.setter
    def cluster(self, cluster: str | None):
        """Set the name of the cluster where the supported group is deployed."""
        self._cluster = cluster

    @property
    def url(self) -> str | None:
        """Get the URL of the supported group."""
        return self._url

    @url.setter
    def url(self, url: str | None):
        """Set the URL of the supported group."""
        self._url = url

    @property
    def test_files(self) -> list[str]:
        """Get the list of test files for the supported group."""
        return self._test_files

    @test_files.setter
    def test_files(self, test_files: list[str]):
        """Set the list of test files for the supported group."""
        self._test_files = test_files

    @property
    def ms_list(self) -> list[ServiceData]:
        """Get the list of microservices that belong to the supported group."""
        return self._ms_list

    @ms_list.setter
    def ms_list(self, ms_list: list[ServiceData]):
        """Set the list of microservices that belong to the supported group."""
        self._ms_list = ms_list

    @property
    def project(self) -> str | None:
        """Get the name of the project that the supported group is part of."""
        return self._project

    @project.setter
    def project(self, project: str | None):
        """Set the name of the project that the supported group is part of."""
        self._project = project
