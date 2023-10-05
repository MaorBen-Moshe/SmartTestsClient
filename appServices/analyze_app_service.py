from models.data_manager import DataManager
from models.group_data import GroupData
from steps.init_services_data_step import init_services_map


class AnalyzeAppService:
    def __init__(self, build_url: str, group_name: str):
        self.data_manager = DataManager()
        self.build_url = build_url
        self.group_name = group_name

    def analyze(self) -> dict[str, GroupData]:
        # load index yaml
        self.data_manager.services_map = init_services_map()

        # load build report data

        # update data per group

        # analyze flows to run

        # prepare response
