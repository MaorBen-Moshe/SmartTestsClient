import os
from threading import Thread

from constants.constants import *
from parsers.yaml_parser import YamlParser


class DataManager:

    def __init__(self):
        self.yaml_parser = YamlParser()
        self.services_map_threads = []
        self.curr_group = None
        self.test_names_by_group = {}
        self.services_map = {}
        self.init_services_map()
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

    def init_services_map(self):
        paths = {
            HELM_INDEX_URL: f"{DATA_DIR}/helm_index.yaml",
            # GREEN_INDEX_URL: f"{DATA_DIR}/green_index.yaml",
        }

        self.services_map_threads = []
        for path in paths:
            t = Thread(target=(lambda: self.yaml_parser.request_yaml_external(path,
                                                                              paths[path],
                                                                              self.services_map)))

            self.services_map_threads.append(t)

        for thread in self.services_map_threads:
            thread.start()

    def get_services_map(self):
        for thread in self.services_map_threads:
            thread.join()

        return self.services_map
