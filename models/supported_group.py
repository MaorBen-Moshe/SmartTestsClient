from __future__ import annotations

from typing import Any

from utils import utils


class SupportedGroup:
    def __init__(self):
        self.group_name: str | None = None
        self.cluster: str | None = None
        self.testng_xml: list[str] = []

    def serialize(self) -> dict[str, Any]:
        return utils.Utils.serialize_class(self, ['testng_xml'])

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
    def testng_xml(self) -> list[str]:
        return self._testng_xml

    @testng_xml.setter
    def testng_xml(self, testng_xml: list[str]):
        self._testng_xml = testng_xml


class SupportedGroupBuilder:
    def __init__(self):
        self.supported_group = SupportedGroup()

    def build(self) -> SupportedGroup:
        return self.supported_group

    def group_name(self, group_name: str | None) -> SupportedGroupBuilder:
        self.supported_group.group_name = group_name
        return self

    def cluster(self, cluster: str | None) -> SupportedGroupBuilder:
        self.supported_group.cluster = cluster
        return self

    def testng_xml(self, testng_xml: list[str]) -> SupportedGroupBuilder:
        self.supported_group.testng_xml = testng_xml
        return self
