from threading import Thread

from constants.constants import HELM_INDEX_URL
from models.service_data import ServiceData
from parsers.yaml_parser import YamlParser


def init_services_map() -> dict[str, ServiceData]:
    yaml_parser = YamlParser()
    services_map = {}

    paths = [
        HELM_INDEX_URL,
        # GREEN_INDEX_URL
    ]

    services_map_threads = []
    for path in paths:
        t = Thread(target=(lambda: yaml_parser.request_yaml_external(path)))

        services_map_threads.append(t)

    for thread in services_map_threads:
        thread.start()

    for thread in services_map_threads:
        thread.join()

    return services_map
