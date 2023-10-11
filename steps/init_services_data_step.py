from __future__ import annotations

from models.service_data import ServiceData
from services.yaml_parser import YamlParserService


class InitServiceMapStep:
    @staticmethod
    def init_services_map(paths: list[str] | None) -> dict[str, ServiceData]:
        yaml_parser = YamlParserService()

        services_map = yaml_parser.request_yaml_external(paths)

        return services_map
