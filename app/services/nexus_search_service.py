from __future__ import annotations

import concurrent.futures
import threading
from distutils.version import LooseVersion
from typing import Any, Iterable

from app import app_main_logger, executor_manager
from app.clients.nexus_client import NexusClient
from app.constants.constants import CONTINUATION_TOKEN, VERSION_KEY, ITEMS_KEY, NEXUS_REPOSITORY_KEY, NEXUS_NAME_KEY
from app.decorators.decorators import log_around
from app.exceptions.excpetions import EmptyInputError
from app.models.service_data import ServiceData
from app.utils.utils import Utils


class NexusSearchService:
    """A class that searches for the latest versions of the microservices from the nexus repository."""

    def __init__(self):
        """Initializes the nexus search service with a nexus client and a lock."""
        self.nexus_client = NexusClient()
        self._lock = threading.Lock()

    @log_around(print_output=True)
    def update_services_master_version(self,
                                       repository: str | None,
                                       ms_list: Iterable[ServiceData]):
        """Updates the master versions of the microservices from the given repository.

        Args:
            repository (str | None): The name of the repository to search from, or None to skip.
            ms_list (Iterable[ServiceData]): The list of microservices to update.

        Raises:
            EmptyInputError: If the repository is None.
        """
        if repository is None:
            raise EmptyInputError("Provided to 'update_services_master_version' repository=None")

        if ms_list:
            futures = []
            for entry in ms_list:
                f = executor_manager.submit(self._get_service_data_for_each_entry, repository, entry)
                futures.append(f)

            concurrent.futures.wait(futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)

    def _get_service_data_for_each_entry(self, repository: str | None,
                                         entry: ServiceData | None):
        """Gets the latest version of a microservice from the repository and updates its entry.

        Args:
            repository (str | None): The name of the repository to search from, or None to skip.
            entry (ServiceData | None): The microservice entry to update, or None to skip.
        """
        if entry is None:
            return

        versions = []
        params = {NEXUS_REPOSITORY_KEY: repository, NEXUS_NAME_KEY: entry.service_name}
        data = self.nexus_client.search_data(params)
        versions = Utils.merge_list(versions, self._get_service_versions(data))
        while data is not None and CONTINUATION_TOKEN in data and data[CONTINUATION_TOKEN] is not None:
            params[CONTINUATION_TOKEN] = data[CONTINUATION_TOKEN]
            data = self.nexus_client.search_data(params)
            versions = Utils.merge_list(versions, self._get_service_versions(data))

        if len(versions) > 0:
            sorted_list = sorted(versions, key=LooseVersion, reverse=True)
            with (self._lock):
                entry.to_version = sorted_list[0]
                entry.from_version = sorted_list[0] if entry.from_version is None else entry.from_version
        else:
            app_main_logger.warning(f"NexusSearchService._get_service_data_for_each_entry():"
                                    f" Failed to get version for {entry.service_name}")

    @classmethod
    def _get_service_versions(cls, data: dict[str, Any]) -> list[str]:
        """Gets the list of versions of a microservice from the data dictionary.

        Args:
            data (dict[str, Any]): The data dictionary to extract the versions from.

        Returns:
            list[str]: The list of versions of the microservice, or an empty list if not found.
        """
        if data is not None and ITEMS_KEY in data and len(data[ITEMS_KEY]) > 0:
            return [item[VERSION_KEY] for item in data[ITEMS_KEY] if
                    VERSION_KEY in item and item[VERSION_KEY] is not None]
        else:
            return []
