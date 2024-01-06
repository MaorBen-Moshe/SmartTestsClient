from __future__ import annotations

from app import app_main_logger, config
from app.decorators.decorators import log_around
from app.models.services_data import ServicesData
from app.services.nexus_search_service import NexusSearchService


class UpdateServiceDataService:

    def __init__(self):
        self.nexus_search_service = NexusSearchService()
        self._supported_services = config.get_supported_services()

    @log_around(print_output=False)
    def update_services_data(self,
                             repository: str | None,
                             services_data: ServicesData | None):
        if services_data is None or len(services_data) == 0:
            app_main_logger.warning("UpdateServiceDataService.update_services_data(): No services data to update.")
            return None

        ms_list = (services_data.get_item(service) for service in services_data)

        ms_list = filter(lambda service: service.pull_request_id is None and (service.to_version == service.from_version
                                                                              or service.to_version is None),
                         ms_list)

        self.nexus_search_service.update_services_master_version(repository, ms_list)

    @log_around(print_output=False)
    def update_from_template(self, services: ServicesData):
        if services is None:
            return

        for service_name in services:
            service = services.get_item(service_name)
            if service is None:
                continue

            supported_service_template = self._supported_services.get_item(service.service_name)

            if supported_service_template is not None:
                service.repo_name = service.repo_name if service.repo_name else supported_service_template.repo_name
                service.project = service.project if service.project else supported_service_template.project
                service.related_group = service.related_group if service.related_group \
                    else supported_service_template.related_group
