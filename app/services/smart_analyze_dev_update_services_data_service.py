from __future__ import annotations

from app.models.service_data import ServiceData
from app.services.nexus_search_service import NexusSearchService


class UpdateServiceDataService:

    def __init__(self):
        self.nexus_search_service = NexusSearchService()

    def update_services_data(self,
                             repository: str | None,
                             services_data: dict[str, ServiceData] | None) -> dict[str, ServiceData] | None:
        if services_data is None or len(services_data) == 0:
            return None

        ms_list = [service for service in services_data
                   if services_data[service].to_version == services_data[service].from_version or
                   services_data[service].to_version is None]

        services_from_nexus = self.nexus_search_service.get_services_master_version(repository, ms_list)

        updated_services_data_map = {}
        for service in services_data:
            service_data = services_data[service]
            if services_data is None:
                continue

            to_version = None
            if (service in services_from_nexus and
                    (services_from_nexus[service].to_version is None or
                     services_from_nexus[service].to_version == services_from_nexus[service].from_version)):
                to_version = services_from_nexus[service].to_version

            updated_services_data_map[service] = (ServiceData.create()
                                                  .from_version(service_data.from_version)
                                                  .to_version(to_version if to_version else service_data.to_version)
                                                  .build())

        return updated_services_data_map
