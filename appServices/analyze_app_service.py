from models.data_manager import DataManager
from models.group_data import GroupData
from services.html_parser import HtmlParserService
from steps.handle_groups_data_step import HandleGroupsDataStep
from steps.init_services_data_step import init_services_map


class AnalyzeAppService:
    def __init__(self, build_url: str, group_name: str):
        self.data_manager = DataManager()
        self.data_manager.set_curr_group(group_name)
        self.handle_group_data_step = HandleGroupsDataStep(self.data_manager.get_filter_for_curr_group())
        self.html_parser = HtmlParserService(build_url)

    def analyze(self) -> dict[str, GroupData]:
        # load index yaml
        self.data_manager.services_map = init_services_map()

        # load build report data
        self.html_parser.load_html(self.data_manager.services_map)

        # update data per group
        self.data_manager.groups_data = self.handle_group_data_step.init_groups_data()

        # analyze flows to run
        self.handle_group_data_step.analyze_flows_per_group(self.data_manager.services_map,
                                                            self.data_manager.groups_data)

        # prepare response
        return self.data_manager.groups_data
