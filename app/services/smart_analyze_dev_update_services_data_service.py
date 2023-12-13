from __future__ import annotations

from app import app_main_logger
from app.models.service_data import ServiceData
from app.models.services_data import ServicesData
from app.services.nexus_search_service import NexusSearchService


class UpdateServiceDataService:

    def __init__(self):
        self.nexus_search_service = NexusSearchService()

    def update_services_data(self,
                             repository: str | None,
                             services_data: ServicesData | None) -> ServicesData | None:
        app_main_logger.debug("UpdateServiceDataService.update_services_data(): Executing UpdateServiceDataStep.")

        if services_data is None or len(services_data) == 0:
            app_main_logger.warning("UpdateServiceDataService.update_services_data(): No services data to update.")
            return None

        ms_list = [service for service in services_data
                   if services_data.get_item(service).to_version ==
                   services_data.get_item(service).from_version or
                   services_data.get_item(service).to_version is None]

        services_from_nexus = self.nexus_search_service.get_services_master_version(repository, ms_list, "DIGOC")

        updated_services_data_map = ServicesData()
        for service in services_data:
            service_data = services_data.get_item(service)
            if services_data is None:
                app_main_logger.warning(f"UpdateServiceDataService.update_services_data(): "
                                        f"Service {service} does not exist in services data.")
                continue

            to_version = None
            if (service in services_from_nexus and
                    (services_from_nexus.get_item(service).to_version is None or
                     services_from_nexus.get_item(service).to_version ==
                     services_from_nexus.get_item(service).from_version)):
                to_version = services_from_nexus.get_item(service).to_version

            updated_services_data_map.add_item(service, (ServiceData.create()
                                                         .from_version(service_data.from_version)
                                                         .to_version(to_version if to_version
                                                                     else service_data.to_version)
                                                         .project(service_data.project)
                                                         .build()))

        app_main_logger.debug(f"UpdateServiceDataService.update_services_data()"
                              f": Response services={updated_services_data_map}")

        return updated_services_data_map
