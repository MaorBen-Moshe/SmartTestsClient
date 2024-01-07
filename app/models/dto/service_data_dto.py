from __future__ import annotations

from app.models.builder import Builder
from app.models.serializable_model import Serializable


class ServiceDataDTO(Serializable):
    """A data transfer object that represents a service and its data flows."""

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
        """Initialize the attributes of the service data."""
        self.service_name: str | None = None
        self.repo_name: str | None = None
        self.from_version: str | None = None
        self.to_version: str | None = None
        self.flows: list[str] = []
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
        """Get the name of the repository where the service code is stored."""
        return self._repo_name

    @repo_name.setter
    def repo_name(self, repo_name: str | None) -> None:
        """Set the name of the repository where the service code is stored."""
        self._repo_name = repo_name

    @property
    def from_version(self) -> str | None:
        """Get the version of the service from which the data flows are generated."""
        return self._from

    @from_version.setter
    def from_version(self, from_version: str | None) -> None:
        """Set the version of the service from which the data flows are generated."""
        self._from = from_version

    @property
    def to_version(self) -> str | None:
        """Get the version of the service to which the data flows are applied."""
        return self._to

    @to_version.setter
    def to_version(self, to_version: str | None) -> None:
        """Set the version of the service to which the data flows are applied."""
        self._to = to_version

    @property
    def flows(self) -> list[str]:
        """Get the list of data flows for the service."""
        return self._flows

    @flows.setter
    def flows(self, flows: list[str]) -> None:
        """Set the list of data flows for the service."""
        self._flows = flows

    @property
    def project(self) -> str | None:
        """Get the name of the project that the service belongs to."""
        return self._project

    @project.setter
    def project(self, project: str | None) -> None:
        """Set the name of the project that the service belongs to."""
        self._project = project

    @property
    def pull_request_id(self) -> str | None:
        """Get the ID of the pull request that contains the service changes."""
        return self._pullRequestId

    @pull_request_id.setter
    def pull_request_id(self, pull_request_id: str | None) -> None:
        """Set the ID of the pull request that contains the service changes."""
        self._pullRequestId = pull_request_id

    @property
    def related_group(self) -> str | None:
        """Get the name of the related group of services that the service is part of."""
        return self._related_group

    @related_group.setter
    def related_group(self, related_group: str | None) -> None:
        """Set the name of the related group of services that the service is part of."""
        self._related_group = related_group

    @staticmethod
    def create():
        """Create a builder object for the service data."""
        return ServiceDataDTOBuilder()


class ServiceDataDTOBuilder(Builder[ServiceDataDTO]):
    """A builder class that helps to construct a service data object."""

    def __init__(self, service_data=None):
        """Initialize the builder with an optional service data object."""
        service_data = service_data if service_data is not None else ServiceDataDTO()
        super().__init__(service_data)

    def service_name(self, service_name: str | None) -> ServiceDataDTOBuilder:
        """Set the name of the service and return the builder."""
        self._item.service_name = service_name
        return self

    def repo_name(self, repo_name: str | None) -> ServiceDataDTOBuilder:
        """Set the name of the repository and return the builder."""
        self._item.repo_name = repo_name
        return self

    def from_version(self, from_version: str | None) -> ServiceDataDTOBuilder:
        """Set the from version of the service and return the builder."""
        self._item.from_version = from_version
        return self

    def to_version(self, to_version: str | None) -> ServiceDataDTOBuilder:
        """Set the to version of the service and return the builder."""
        self._item.to_version = to_version
        return self

    def flows(self, flows: list[str]) -> ServiceDataDTOBuilder:
        """Set the list of data flows and return the builder."""
        self._item.flows = flows
        return self

    def project(self, project: str | None) -> ServiceDataDTOBuilder:
        """Set the name of the project and return the builder."""
        self._item.project = project
        return self

    def pull_request_id(self, pull_request_id: str | None) -> ServiceDataDTOBuilder:
        """Set the ID of the pull request and return the builder."""
        self._item.pull_request_id = pull_request_id
        return self

    def related_group(self, related_group: str | None) -> ServiceDataDTOBuilder:
        """Set the name of the related group and return the builder."""
        self._item.related_group = related_group
        return self
