from __future__ import annotations

import os
import urllib


class Utils:
    @staticmethod
    def create_filter_by_list(values: list[str] | None) -> str:
        if values is None or len(values) == 0:
            return ""

        values = [f".*{value}.*" for value in values]
        return "|".join(values)

    @staticmethod
    def is_valid_url(url):
        parsed = urllib.parse.urlparse(url)
        ext = os.path.splitext(parsed.path)[1]
        if ext in [".zip", ".html"]:
            return True

        return False

    @staticmethod
    def serialize_class(cls, ignored_fields: list[str]):
        if cls is None:
            return None

        return (dict(
            (i.replace(cls.__class__.__name__, '').lstrip("_"), value)
            for i, value in cls.__dict__.items()
            if i.replace(cls.__class__.__name__, '').lstrip("_") not in ignored_fields
        ))

    @staticmethod
    def add_flows_without_duplications(flows: list[str], curr_flows: list[str] | None) -> list[str]:
        if curr_flows is None or len(curr_flows) == 0:
            return flows

        filtered_flows = [curr_flow for curr_flow in curr_flows if curr_flow not in flows]
        flows.extend(filtered_flows)
