from __future__ import annotations

from app.models.service_data import ServiceData
from app.services.html_parser_service import HtmlParserService


class HtmlParserStep:
    def __init__(self, build_url: str | None):
        self.html_parser_service = HtmlParserService()
        self.build_url = build_url

    def load_html_step(self, services_map: dict[str, ServiceData] | None, filtered_ms_list: list[str]):
        self.html_parser_service.load_html(self.build_url, services_map, filtered_ms_list)