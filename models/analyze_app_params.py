from __future__ import annotations


class AnalyzeAppServiceParameters:
    def __init__(self):
        self.build_url: str | None = None
        self.group_name: str | None = None


class AnalyzeAppServiceParametersBuilder:
    def __init__(self):
        self.parameters = AnalyzeAppServiceParameters()

    def build(self) -> AnalyzeAppServiceParameters:
        return self.parameters

    def group_name(self, group_name: str | None) -> AnalyzeAppServiceParametersBuilder:
        self.parameters.group_name = group_name
        return self

    def build_url(self, build_url: str | None) -> AnalyzeAppServiceParametersBuilder:
        self.parameters.build_url = build_url
        return self
