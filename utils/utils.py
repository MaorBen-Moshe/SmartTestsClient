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
        if ext in [".zip", ".yaml", ".html"]:
            return True

        return False
