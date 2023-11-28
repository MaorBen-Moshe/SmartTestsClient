from __future__ import annotations

from app.models.service_data import ServiceData
from app.services.nexus_search_service import NexusSearchService


class InitServiceMapStep:
    @staticmethod
    def init_services_map(repository: str | None, filtered_ms_list: list[str]) -> dict[str, ServiceData]:
        nexus_search = NexusSearchService()

        services_map = nexus_search.get_services_master_version(repository, filtered_ms_list)

        return services_map
