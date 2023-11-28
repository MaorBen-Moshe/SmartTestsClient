from __future__ import annotations

from typing import Any

from app.models.builder import Builder
from app.utils import utils


class SupportedGroup:
    def __init__(self):
        self.group_name: str | None = None
        self.cluster: str | None = None
        self.testng_xml: list[str] = []
        self.url: str | None = None

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
    def url(self) -> str | None:
        return self._url

    @url.setter
    def url(self, url: str | None):
        self._url = url

    @property
    def testng_xml(self) -> list[str]:
        return self._testng_xml

    @testng_xml.setter
    def testng_xml(self, testng_xml: list[str]):
        self._testng_xml = testng_xml

    @staticmethod
    def create():
        return SupportedGroupBuilder()


class SupportedGroupBuilder(Builder[SupportedGroup]):
    def __init__(self, supported_group=None):
        supported_group = supported_group if supported_group is not None else SupportedGroup()
        super().__init__(supported_group)

    def group_name(self, group_name: str | None) -> SupportedGroupBuilder:
        self.item.group_name = group_name
        return self

    def cluster(self, cluster: str | None) -> SupportedGroupBuilder:
        self.item.cluster = cluster
        return self

    def url(self, url: str | None) -> SupportedGroupBuilder:
        self.item.url = url
        return self

    def testng_xml(self, testng_xml: list[str]) -> SupportedGroupBuilder:
        self.item.testng_xml = testng_xml
        return self