from __future__ import annotations


class Utils:
    @staticmethod
    def create_filter_by_list(values: list[str] | None) -> str:
        if values is None or len(values) == 0:
            return ""

        values = [f".*{value}.*" for value in values]
        return "|".join(values)
