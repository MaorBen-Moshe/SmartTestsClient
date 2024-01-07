from __future__ import annotations

from app import app_main_logger, config
from app.decorators.decorators import log_around
from app.models.services_data import ServicesData
from app.services.nexus_search_service import NexusSearchService


class UpdateServiceDataService:
    """A class that updates the services data with the latest versions and the template values from the config."""

    def __init__(self):
        """Initializes the update service data service with a nexus search service and a supported services object."""
        self.nexus_search_service = NexusSearchService()
        self._supported_services = config.get_supported_services()

    @log_around(print_output=False)
    def update_services_data(self,
                             repository: str | None,
                             services_data: ServicesData | None):
        """Updates the services data with the latest versions of the microservices from the given repository.

        Args:
            repository (str | None): The name of the repository to search from, or None to skip.
            services_data (ServicesData | None): The services data to update, or None to skip.
        """
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
        """Updates the services data with the template values from the config.

        Args:
            services (ServicesData): The services data to update.
        """
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
