from __future__ import annotations

from models.service_data import ServiceData
from services.html_parser_service import HtmlParserService


class HtmlParserStep:
    def __init__(self, build_url: str | None):
        self.html_parser_service = HtmlParserService()
        self.build_url = build_url

    def load_html_step(self, services_map: dict[str, ServiceData] | None):
        self.html_parser_service.load_html(self.build_url, services_map)
