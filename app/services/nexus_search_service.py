from __future__ import annotations

from typing import Any
from distutils.version import LooseVersion
from app.clients.nexus_client import NexusClient
from app.constants.constants import CONTINUATION_TOKEN, VERSION_KEY, ITEMS_KEY
from app.exceptions.excpetions import EmptyInputError
from app.models.service_data import ServiceData


class NexusSearchService:
    def __init__(self):
        self.services_map: dict[str, ServiceData] = {}
        self.nexus_client = NexusClient()

    def get_services_master_version(self,
                                    repository: str | None,
                                    filtered_ms_list: list[str] | None) -> dict[str, ServiceData]:
        if repository is None:
            raise EmptyInputError("Provided to 'get_services_master_version' repository=None")

        if filtered_ms_list:
            for entry in filtered_ms_list:
                versions = []
                params = {'repository': repository, 'name': entry}
                data = self.nexus_client.search_data(params)
                versions = self._merge_list(versions, self._get_service_versions(data))
                while data is not None and CONTINUATION_TOKEN in data and data[CONTINUATION_TOKEN] is not None:
                    params[CONTINUATION_TOKEN] = data[CONTINUATION_TOKEN]
                    data = self.nexus_client.search_data(params)
                    versions = self._merge_list(versions, self._get_service_versions(data))

                if len(versions) > 0:
                    sorted_list = sorted(versions, key=LooseVersion, reverse=True)
                    self.services_map[entry] = (ServiceData.create()
                                                .new_version(sorted_list[0])
                                                .old_version(sorted_list[0])
                                                .build())

        return self.services_map

    @staticmethod
    def _get_service_versions(data: dict[str, Any]) -> list[str]:
        if data is not None and ITEMS_KEY in data and len(data[ITEMS_KEY]) > 0:
            return [item[VERSION_KEY] for item in data[ITEMS_KEY] if VERSION_KEY in item and item[VERSION_KEY] is not None]
        else:
            return []

    @staticmethod
    def _merge_list(list_to: list[str], list_from: list[str]) -> list[str]:
        return list(set(list_to + list_from))
