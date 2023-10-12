from __future__ import annotations

from models.config_manager import ConfigManager
from models.data_manager import DataManager
from models.group_data import GroupData
from steps.handle_groups_data_step import HandleGroupsDataStep
from steps.html_parser_step import HtmlParserStep
from steps.init_services_data_step import InitServiceMapStep


class AnalyzeAppService:
    def __init__(self, build_url: str | None, group_name: str | None):
        self.data_manager = DataManager()
        self.data_manager.set_curr_group(group_name)
        self.handle_group_data_step = HandleGroupsDataStep(self.data_manager.get_filter_for_curr_group())
        self.html_parser = HtmlParserStep(build_url)
        self.config_manager = ConfigManager()

    def analyze(self) -> dict[str, GroupData]:
        # load index yaml
        self.data_manager.services_map = InitServiceMapStep.init_services_map(self.config_manager.get_index_data_urls())

        # load build report data
        self.html_parser.load_html_step(self.data_manager.services_map)

        # update data per group
        self.data_manager.groups_data = self.handle_group_data_step.init_groups_data()

        # analyze flows to run
        self.handle_group_data_step.analyze_flows_per_group(self.data_manager.services_map,
                                                            self.data_manager.groups_data)

        # prepare response
        return {key: self.data_manager.groups_data.get(key).serialize() for key in self.data_manager.groups_data}
