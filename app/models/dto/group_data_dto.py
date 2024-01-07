from __future__ import annotations

from app.models.serializable_model import Serializable


class GroupDataDTO(Serializable):
    """A data transfer object that represents a group of data flows."""

    __slots__ = [
        "_test_xml_name",
        "_test_xml_path",
        "_total_flows_count",
        "_curr_flows_count",
        "_flows",
    ]

    def __init__(self):
        """Initialize the attributes of the group data."""
        self.test_xml_name: str | None = None
        self.test_xml_path: str | None = None
        self.total_flows_count: int = 0
        self.curr_flows_count: int = 0
        self.flows: list[str] = []

    @property
    def test_xml_name(self) -> str | None:
        """Get the name of the test XML file for the group data."""
        return self._test_xml_name

    @test_xml_name.setter
    def test_xml_name(self, test_xml_name: str | None):
        """Set the name of the test XML file for the group data."""
        self._test_xml_name = test_xml_name

    @property
    def test_xml_path(self) -> str | None:
        """Get the path of the test XML file for the group data."""
        return self._test_xml_path

    @test_xml_path.setter
    def test_xml_path(self, test_xml_path: str | None):
        """Set the path of the test XML file for the group data."""
        self._test_xml_path = test_xml_path

    @property
    def total_flows_count(self) -> int:
        """Get the total number of data flows in the group."""
        return self._total_flows_count

    @total_flows_count.setter
    def total_flows_count(self, total_flows_count: int):
        """Set the total number of data flows in the group."""
        self._total_flows_count = total_flows_count

    @property
    def curr_flows_count(self) -> int:
        """Get the current number of data flows in the group."""
        return self._curr_flows_count

    @curr_flows_count.setter
    def curr_flows_count(self, curr_flows_count: int):
        """Set the current number of data flows in the group."""
        self._curr_flows_count = curr_flows_count

    @property
    def flows(self) -> list[str] | None:
        """Get the list of data flows in the group."""
        return self._flows

    @flows.setter
    def flows(self, flows: list[str] | None):
        """Set the list of data flows in the group."""
        self._flows = flows
