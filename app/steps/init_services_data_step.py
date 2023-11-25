from __future__ import annotations

from app.models.service_data import ServiceData
from app.services.yaml_parser_service import YamlParserService


class InitServiceMapStep:
    @staticmethod
    def init_services_map(paths: list[str] | None, filtered_ms_list: list[str]) -> dict[str, ServiceData]:
        yaml_parser = YamlParserService()

        services_map = yaml_parser.request_yaml_external(paths, filtered_ms_list)

        return services_map
