from threading import Thread

from models.config_manager import ConfigManager
from models.service_data import ServiceData
from parsers.yaml_parser import YamlParser


def init_services_map() -> dict[str, ServiceData]:
    yaml_parser = YamlParser()
    services_map = {}

    config = ConfigManager()
    paths = [
        config.get_helm_index_url(),
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
