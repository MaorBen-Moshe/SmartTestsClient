from __future__ import annotations

from app.models.builder import Builder
from app.models.serializable_model import Serializable
from app.utils.utils import Utils


class GroupData(Serializable):
    """A class that represents a group of test flows with a name and a path."""

    __slots__ = [
        "_test_xml_name",
        "_test_xml_path",
        "_total_flows_count",
        "_curr_flows_count",
        "_flows"
    ]

    def __init__(self):
        """Initializes the group data with None values for the name and the path, and zero values for the counts."""
        self.test_xml_name = None
        self.test_xml_path = None
        self.total_flows_count = 0
        self.curr_flows_count = 0
        self.flows = []

    @property
    def test_xml_name(self) -> str | None:
        """Gets or sets the name of the test XML file.

        Returns:
            str | None: The name of the test XML file, or None if not set.
        """
        return self._test_xml_name

    @test_xml_name.setter
    def test_xml_name(self, test_xml_name: str | None):
        """Sets the name of the test XML file.

        Args:
            test_xml_name (str | None): The name of the test XML file, or None to unset it.
        """
        self._test_xml_name = test_xml_name

    @property
    def test_xml_path(self) -> str | None:
        """Gets or sets the path of the test XML file.

        Returns:
            str | None: The path of the test XML file, or None if not set.
        """
        return self._test_xml_path

    @test_xml_path.setter
    def test_xml_path(self, test_xml_path: str | None):
        """Sets the path of the test XML file.

        Args:
            test_xml_path (str | None): The path of the test XML file, or None to unset it.
        """
        self._test_xml_path = test_xml_path

    @property
    def total_flows_count(self) -> int:
        """Gets or sets the total number of test flows in the group.

        Returns:
            int: The total number of test flows in the group.
        """
        return self._total_flows_count

    @total_flows_count.setter
    def total_flows_count(self, total_flows_count: int):
        """Sets the total number of test flows in the group.

        Args:
            total_flows_count (int): The total number of test flows in the group.
        """
        self._total_flows_count = total_flows_count

    @property
    def curr_flows_count(self) -> int:
        """Gets or sets the current number of test flows in the group.

        Returns:
            int: The current number of test flows in the group.
        """
        return self._curr_flows_count

    @curr_flows_count.setter
    def curr_flows_count(self, curr_flows_count: int):
        """Sets the current number of test flows in the group.

        Args:
            curr_flows_count (int): The current number of test flows in the group.
        """
        self._curr_flows_count = curr_flows_count

    @property
    def flows(self) -> list[str] | None:
        """Gets or sets the list of test flows in the group.

        Returns:
            list[str] | None: The list of test flows in the group, or None if not set.
        """
        return self._flows

    @flows.setter
    def flows(self, flows: list[str] | None):
        """Sets the list of test flows in the group.

        Args:
            flows (list[str] | None): The list of test flows in the group, or None to unset it.
        """
        self._flows = flows

    def add_flows(self, curr_flows: list[str] | None):
        """Adds the given test flows to the group without duplications.

        Args:
            curr_flows (list[str] | None): The list of test flows to add, or None to skip.
        """
        Utils.add_flows_without_duplications(self.flows, curr_flows)
        self.curr_flows_count = len(self.flows)

    @staticmethod
    def create():
        """Creates a new group data builder.

        Returns:
            GroupDataBuilder: A group data builder instance.
        """
        return GroupDataBuilder()


class GroupDataBuilder(Builder[GroupData]):
    """A class that builds a group data instance."""

    def __init__(self, group_data=None):
        """Initializes the group data builder with a group data instance.

        Args:
            group_data (GroupData | None): The group data instance to build, or None to create a new one.
        """
        group_data = group_data if group_data is not None else GroupData()
        super().__init__(group_data)

    def test_xml_name(self, test_xml_name: str | None) -> GroupDataBuilder:
        """Sets the name of the test XML file for the group data to build.

        Args:
            test_xml_name (str | None): The name of the test XML file, or None to unset it.

        Returns:
            GroupDataBuilder: The same group data builder instance, for method chaining.
        """
        self._item.test_xml_name = test_xml_name
        return self

    def test_xml_path(self, test_xml_path: str | None) -> GroupDataBuilder:
        """Sets the path of the test XML file for the group data to build.

        Args:
            test_xml_path (str | None): The path of the test XML file, or None to unset it.

        Returns:
            GroupDataBuilder: The same group data builder instance, for method chaining.
        """
        self._item.test_xml_path = test_xml_path
        return self

    def total_flows_count(self, total_flows_count: int) -> GroupDataBuilder:
        """Sets the total number of test flows for the group data to build.

        Args:
            total_flows_count (int): The total number of test flows for the group data to build.

        Returns:
            GroupDataBuilder: The same group data builder instance, for method chaining.
        """
        self._item.total_flows_count = total_flows_count
        return self

    def flows(self, flows: list[str] | None) -> GroupDataBuilder:
        """Sets the list of test flows for the group data to build.

        Args:
            flows (list[str] | None): The list of test flows for the group data to build, or None to unset it.

        Returns:
            GroupDataBuilder: The same group data builder instance, for method chaining.
        """
        self._item.flows = flows
        self._item.curr_flows_count = len(flows) if flows is not None else 0
        return self
