from constants.constants import *
from models.group_data import GroupData
from models.service_data import ServiceData


class DataManager:

    def __init__(self):
        self.curr_group = None
        self.test_names_by_group = {}
        self.services_map: dict[str, ServiceData] = {}
        self.filter_by_group = {
            "oc-cd-group4-coc-include-ed": GROUP4_XML,
        }
        self.groups_data: dict[str, GroupData] = {}

    def set_curr_group(self, group_name):
        self.curr_group = group_name

    def get_filter_for_curr_group(self):
        if self.curr_group is None:
            return None

        return self.filter_by_group[self.curr_group]

    def get_tests_total_count(self):
        return sum([len(self.test_names_by_group[test_group]) for test_group in self.test_names_by_group])

    def get_services_map(self):
        return self.services_map
