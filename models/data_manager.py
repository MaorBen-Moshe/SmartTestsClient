import os
from threading import Thread

from constants.constants import *
from parsers.yaml_parser import YamlParser


class DataManager:

    def __init__(self):
        self.curr_group = None
        self.test_names_by_group = {}
        self.services_map = {}
        self.filter_by_group = {
            "all": "",
            "group4": GROUP4_XML,
        }

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

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
