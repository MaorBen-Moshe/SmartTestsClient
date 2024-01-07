from __future__ import annotations

from app.models.builder import Builder
from app.models.serializable_model import Serializable
from app.utils.utils import Utils


class ServiceData(Serializable):
    """A class that represents the data of a service."""

    __slots__ = [
        "_service_name",
        "_repo_name",
        "_from",
        "_to",
        "_flows",
        "_project",
        "_pullRequestId",
        "_related_group",
    ]

    def __init__(self):
        """Initialize the attributes with default values."""
        self.service_name: str | None = None
        self.repo_name: str | None = None
        self.from_version: str | None = None
        self.to_version: str | None = None
        self.flows = []
        self.project: str | None = None
        self.pull_request_id: str | None = None
        self.related_group: str | None = None

    @property
    def service_name(self) -> str | None:
        """Get the name of the service."""
        return self._service_name

    @service_name.setter
    def service_name(self, service_name: str | None) -> None:
        """Set the name of the service."""
        self._service_name = service_name

    @property
    def repo_name(self) -> str | None:
        """Get the name of the repository."""
        return self._repo_name

    @repo_name.setter
    def repo_name(self, repo_name: str | None) -> None:
        """Set the name of the repository."""
        self._repo_name = repo_name

    @property
    def from_version(self) -> str | None:
        """Get the 'from' version of the service."""
        return self._from

    @from_version.setter
    def from_version(self, from_version: str | None) -> None:
        """Set the 'from' version of the service."""
        self._from = from_version

    @property
    def to_version(self) -> str | None:
        """Get the 'to' version of the service."""
        return self._to

    @to_version.setter
    def to_version(self, to_version: str | None) -> None:
        """Set the 'to' version of the service."""
        self._to = to_version

    @property
    def flows(self) -> list[str]:
        """Get the list of flows for the service."""
        return self._flows

    @flows.setter
    def flows(self, flows: list[str]) -> None:
        """Set the list of flows for the service."""
        self._flows = flows

    @property
    def project(self) -> str | None:
        """Get the name of the project."""
        return self._project

    @project.setter
    def project(self, project: str | None) -> None:
        """Set the name of the project."""
        self._project = project

    @property
    def pull_request_id(self) -> str | None:
        """Get the id of the pull request."""
        return self._pullRequestId

    @pull_request_id.setter
    def pull_request_id(self, pull_request_id: str | None) -> None:
        """Set the id of the pull request."""
        self._pullRequestId = pull_request_id

    @property
    def related_group(self) -> str | None:
        """Get the name of the related group."""
        return self._related_group

    @related_group.setter
    def related_group(self, related_group: str | None) -> None:
        """Set the name of the related group."""
        self._related_group = related_group

    def add_flows(self, curr_flows: list[str] | None):
        """Add the current flows to the existing flows without duplications."""
        self.flows = self.flows if self.flows is not None else []
        Utils.add_flows_without_duplications(self.flows, curr_flows)

    @staticmethod
    def create():
        """Create a new instance of the class using a builder."""
        return ServiceDataBuilder()


class ServiceDataBuilder(Builder[ServiceData]):
    """A builder class for creating ServiceData instances."""

    def __init__(self, service_data=None):
        """Initialize the builder with an optional service data instance."""
        service_data = service_data if service_data is not None else ServiceData()
        super().__init__(service_data)

    def service_name(self, service_name: str | None) -> ServiceDataBuilder:
        """Set the name of the service and return the builder."""
        self._item.service_name = service_name
        return self

    def repo_name(self, repo_name: str | None) -> ServiceDataBuilder:
        """Set the name of the repository and return the builder."""
        self._item.repo_name = repo_name
        return self

    def from_version(self, from_version: str | None) -> ServiceDataBuilder:
        """Set the 'from' version of the service and return the builder."""
        self._item.from_version = from_version
        return self

    def to_version(self, to_version: str | None) -> ServiceDataBuilder:
        """Set the 'to' version of the service and return the builder."""
        self._item.to_version = to_version
        return self

    def flows(self, flows: list[str]) -> ServiceDataBuilder:
        """Set the list of flows for the service and return the builder."""
        self._item.flows = flows if flows is not None else []
        return self

    def project(self, project: str | None) -> ServiceDataBuilder:
        """Set the name of the project and return the builder."""
        self._item.project = project
        return self

    def pull_request_id(self, pull_request_id: str | None) -> ServiceDataBuilder:
        """Set the id of the pull request and return the builder."""
        self._item.pull_request_id = pull_request_id
        return self

    def related_group(self, related_group: str | None) -> ServiceDataBuilder:
        """Set the name of the related group and return the builder."""
        self._item.related_group = related_group
        return self
