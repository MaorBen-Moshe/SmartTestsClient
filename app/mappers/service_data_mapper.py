from __future__ import annotations

from typing import Any

from app.constants.constants import SERVICE_NAME_KEY, SERVICE_FROM_KEY, SERVICE_TO_KEY, PULL_REQUEST_ID_KEY, \
    SERVICE_FLOWS_KEY, SERVICE_PROJECT_KEY, SERVICE_REPO_NAME_KEY
from app.models.dto.service_data_dto import ServiceDataDTO
from app.models.service_data import ServiceData
from app.models.services_data import ServicesData


class ServiceDataMapper:
    """A class that maps between ServiceData and ServiceDataDTO objects."""

    @classmethod
    def map_from_dict_list_to_dto(cls, service_data_dict: list[dict[str, Any]]) -> list[ServiceDataDTO]:
        """Maps a list of dictionaries to a list of ServiceDataDTO objects.

        Args:
            service_data_dict (list[dict[str, Any]]): A list of dictionaries containing service data, or None.

        Returns:
            list[ServiceDataDTO]: A list of ServiceDataDTO objects, or an empty list if the input is None or invalid.
        """
        service_data_dto_list = []
        if service_data_dict and type(service_data_dict) is list:
            for service_data in service_data_dict:
                if service_data is not None and type(service_data) is dict:
                    service_data_dto_list.append(cls.map_from_dict_to_dto(service_data))
        return service_data_dto_list

    @classmethod
    def map_from_dict_to_dto(cls, service_data_dict: dict[str, Any]) -> ServiceDataDTO | None:
        """Maps a dictionary to a ServiceDataDTO object.

        Args:
            service_data_dict (dict[str, Any]): A dictionary containing service data, or None.

        Returns:
            ServiceDataDTO | None: A ServiceDataDTO object, or None if the input is None or invalid.
        """
        if service_data_dict is None or type(service_data_dict) is not dict:
            return None

        service_data_dto = ServiceDataDTO()
        service_data_dto.service_name = service_data_dict.get(SERVICE_NAME_KEY)
        service_data_dto.repo_name = service_data_dict.get(SERVICE_REPO_NAME_KEY)
        service_data_dto.from_version = service_data_dict.get(SERVICE_FROM_KEY)
        service_data_dto.to_version = service_data_dict.get(SERVICE_TO_KEY)
        service_data_dto.flows = service_data_dict.get(SERVICE_FLOWS_KEY)
        service_data_dto.project = service_data_dict.get(SERVICE_PROJECT_KEY)
        service_data_dto.pull_request_id = service_data_dict.get(PULL_REQUEST_ID_KEY)
        return service_data_dto

    @classmethod
    def map_from_dto_to_services_data(cls, services_data_dto: list[ServiceDataDTO]) -> ServicesData:
        """Maps a list of ServiceDataDTO objects to a ServicesData object.

        Args:
            services_data_dto (list[ServiceDataDTO]): A list of ServiceDataDTO objects, or None.

        Returns:
            ServicesData: A ServicesData object, or an empty ServicesData object if the input is None or invalid.
        """
        services_data = ServicesData()
        if services_data_dto and type(services_data_dto) is list:
            for service_data_dto in services_data_dto:
                if service_data_dto is not None and type(service_data_dto) is ServiceDataDTO:
                    services_data.add_item(service_data_dto.service_name, cls.map_from_dto(service_data_dto))
        return services_data

    @classmethod
    def map_from_services_data_to_dto_list(cls, services_data: ServicesData) -> list[ServiceDataDTO]:
        """Maps a ServicesData object to a list of ServiceDataDTO objects.

        Args:
            services_data (ServicesData): A ServicesData object, or None.

        Returns:
            list[ServiceDataDTO]: A list of ServiceDataDTO objects, or an empty list if the input is None or invalid.
        """
        services_data_dto_list = []
        if services_data and type(services_data) is ServicesData:
            for service_name in services_data:
                service_data = services_data.get_item(service_name)
                if service_data is not None and type(service_data) is ServiceData:
                    services_data_dto_list.append(cls.map_from_service_data_to_dto(service_data))
        return services_data_dto_list

    @classmethod
    def map_from_dto(cls, service_data_dto: ServiceDataDTO | None) -> ServiceData | None:
        """Maps a ServiceDataDTO object to a ServiceData object.

        Args:
            service_data_dto (ServiceDataDTO | None): A ServiceDataDTO object, or None.

        Returns:
            ServiceData | None: A ServiceData object, or None if the input is None or invalid.
        """
        if service_data_dto is None or type(service_data_dto) is not ServiceDataDTO:
            return None

        service_data = ServiceData()
        service_data.service_name = service_data_dto.service_name
        service_data.repo_name = service_data_dto.repo_name
        service_data.from_version = service_data_dto.from_version
        service_data.to_version = service_data_dto.to_version
        service_data.flows = service_data_dto.flows
        service_data.project = service_data_dto.project
        service_data.pull_request_id = service_data_dto.pull_request_id
        service_data.related_group = service_data_dto.related_group
        return service_data

    @classmethod
    def map_from_service_data_to_dto(cls, service_data: ServiceData | None) -> ServiceDataDTO | None:
        """Maps a ServiceData object to a ServiceDataDTO object.

        Args:
            service_data (ServiceData | None): A ServiceData object, or None.

        Returns:
            ServiceDataDTO | None: A ServiceDataDTO object, or None if the input is None or invalid.
        """
        if service_data is None or type(service_data) is not ServiceData:
            return None

        service_data_dto = ServiceDataDTO()
        service_data_dto.service_name = service_data.service_name
        service_data_dto.repo_name = service_data.repo_name
        service_data_dto.from_version = service_data.from_version
        service_data_dto.to_version = service_data.to_version
        service_data_dto.flows = service_data.flows
        service_data_dto.project = service_data.project
        service_data_dto.pull_request_id = service_data.pull_request_id
        service_data_dto.related_group = service_data.related_group
        return service_data_dto
