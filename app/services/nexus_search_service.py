from __future__ import annotations

from app.clients.nexus_client import NexusClient
from app.exceptions.excpetions import EmptyInputError
from app.models.service_data import ServiceData


class NexusSearchService:
    def __init__(self):
        self.services_map: dict[str, ServiceData] = {}
        self.nexus_client = NexusClient()

    def get_services_master_version(self, repository: str | None, filtered_ms_list: list[str] | None) -> dict[str, ServiceData]:
        if repository is None:
            raise EmptyInputError("Provided to 'get_services_master_version' None repository")

        if filtered_ms_list:
            for entry in filtered_ms_list:
                params = {'repository': repository, 'name': entry}
                data = self.nexus_client.search_data(params)
                while data is not None and 'continuationToken' in data and data['continuationToken'] is not None:
                    params['continuationToken'] = data['continuationToken']
                    data = self.nexus_client.search_data(params)

                if data is not None and 'items' in data and len(data['items']) > 0:
                    version = data['items'][-1]['version'] if 'version' in data['items'][-1] else None
                    self.services_map[entry] = (ServiceData.create().new_version(version)
                                                .old_version(version)
                                                .build())

        return self.services_map
