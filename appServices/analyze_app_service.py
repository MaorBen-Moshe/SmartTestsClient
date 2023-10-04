from models.data_manager import DataManager
from models.group_data import GroupData


class AnalyzeAppService:
    def __init__(self, build_url: str, group_name: str):
        self.data_manager = DataManager()
        self.build_url = build_url
        self.group_name = group_name

    def analyze(self) -> dict[str, GroupData]:
        # load index yaml ( parallel )
        # load build report data
        # update data per group
        # analyze flows to run
        # prepare response
        pass
