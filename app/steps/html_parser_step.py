from __future__ import annotations

from app.models.service_data import ServiceData
from app.services.html_parser_service import HtmlParserService


class HtmlParserStep:
    def __init__(self):
        self.html_parser_service = HtmlParserService()

    def load_html_step(self, build_url: str | None,
                       services_map: dict[str, ServiceData] | None,
                       filtered_ms_list: list[str]):
        self.html_parser_service.load_html(build_url, services_map, filtered_ms_list)
