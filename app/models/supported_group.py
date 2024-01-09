from __future__ import annotations

from app.models.builder import Builder
from app.models.services_data import ServicesData


class SupportedGroup:
    """A class that represents a supported group of services."""

    __slots__ = [
        "_namespace",
        "_cluster",
        "_test_files",
        "_url",
        "_services_data",
        "_project",
    ]

    def __init__(self):
        self.namespace: str | None = None
        self.cluster: str | None = None
        self.test_files: list[str] = []
        self.url: str | None = None
        self.services_data: ServicesData = ServicesData()
        self.project: str | None = None

    @property
    def namespace(self) -> str | None:
        """Gets or sets the group namespace.

        Returns:
            str | None: The name of the group, or None if not set.
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace: str | None):
        """Sets the group namespace.

        Args:
            namespace (str | None): The group namespace, or None to unset it.
        """
        self._namespace = namespace

    @property
    def cluster(self) -> str | None:
        """Gets or sets the cluster of the group.

        Returns:
            str | None: The cluster of the group, or None if not set.
        """
        return self._cluster

    @cluster.setter
    def cluster(self, cluster: str | None):
        """Sets the cluster of the group.

        Args:
            cluster (str | None): The cluster of the group, or None to unset it.
        """
        self._cluster = cluster

    @property
    def url(self) -> str | None:
        """Gets or sets the URL of the group.

        Returns:
            str | None: The URL of the group, or None if not set.
        """
        return self._url

    @url.setter
    def url(self, url: str | None):
        """Sets the URL of the group.

        Args:
            url (str | None): The URL of the group, or None to unset it.
        """
        self._url = url

    @property
    def test_files(self) -> list[str]:
        """Gets or sets the list of test files for the group.

        Returns:
            list[str]: The list of test files for the group, or an empty list if not set.
        """
        return self._test_files

    @test_files.setter
    def test_files(self, test_files: list[str]):
        """Sets the list of test files for the group.

        Args:
            test_files (list[str]): The list of test files for the group.
        """
        self._test_files = test_files

    @property
    def services_data(self) -> ServicesData:
        """Gets or sets the services data for the group.

        Returns:
            ServicesData: The services data for the group, or an empty ServicesData instance if not set.
        """
        return self._services_data

    @services_data.setter
    def services_data(self, services_data: ServicesData):
        """Sets the services data for the group.

        Args:
            services_data (ServicesData): The services data for the group.
        """
        self._services_data = services_data

    @property
    def project(self) -> str | None:
        """Gets or sets the project of the group.

        Returns:
            str | None: The project of the group, or None if not set.
        """
        return self._project

    @project.setter
    def project(self, project: str | None):
        """Sets the project of the group.

        Args:
            project (str | None): The project of the group, or None to unset it.
        """
        self._project = project

    @staticmethod
    def create():
        """Creates a new supported group builder.

        Returns:
            SupportedGroupBuilder: A supported group builder instance.
        """
        return SupportedGroupBuilder()


class SupportedGroupBuilder(Builder[SupportedGroup]):
    """A class that builds a supported group instance."""

    def __init__(self, supported_group=None):
        supported_group = supported_group if supported_group is not None else SupportedGroup()
        super().__init__(supported_group)

    def namespace(self, namespace: str | None) -> SupportedGroupBuilder:
        """Sets the group namespace to build.

        Args:
            namespace (str | None): The group namespace, or None to unset it.

        Returns:
            SupportedGroupBuilder: The same supported group builder instance, for method chaining.
        """
        self._item.namespace = namespace
        return self

    def cluster(self, cluster: str | None) -> SupportedGroupBuilder:
        """Sets the cluster of the group to build.

        Args:
            cluster (str | None): The cluster of the group, or None to unset it.

        Returns:
            SupportedGroupBuilder: The same supported group builder instance, for method chaining.
        """
        self._item.cluster = cluster
        return self

    def url(self, url: str | None) -> SupportedGroupBuilder:
        """Sets the URL of the group to build.

        Args:
            url (str | None): The URL of the group, or None to unset it.

        Returns:
            SupportedGroupBuilder: The same supported group builder instance, for method chaining.
        """
        self._item.url = url
        return self

    def test_files(self, test_files: list[str]) -> SupportedGroupBuilder:
        """Sets the list of test files for the group to build.

        Args:
            test_files (list[str]): The list of test files for the group.

        Returns:
            SupportedGroupBuilder: The same supported group builder instance, for method chaining.
        """
        self._item.test_files = test_files
        return self

    def services_data(self, services_data: ServicesData) -> SupportedGroupBuilder:
        """Sets the services data for the group to build.

        Args:
            services_data (ServicesData): The services data for the group.

        Returns:
            SupportedGroupBuilder: The same supported group builder instance, for method chaining.
        """
        self._item.services_data = services_data
        return self

    def project(self, project: str | None) -> SupportedGroupBuilder:
        """Sets the project of the group to build.

        Args:
            project (str | None): The project of the group, or None to unset it.

        Returns:
            SupportedGroupBuilder: The same supported group builder instance, for method chaining.
        """
        self._item.project = project
        return self
