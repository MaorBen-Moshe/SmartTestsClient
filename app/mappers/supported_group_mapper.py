from __future__ import annotations

from app.models.dto.supported_group_dto import SupportedGroupDTO
from app.models.supported_group import SupportedGroup


class SupportedGroupMapper:
    """A class that maps between SupportedGroup and SupportedGroupDTO objects."""

    @classmethod
    def map_to_dto(cls, supported_group: SupportedGroup) -> SupportedGroupDTO | None:
        """Maps a SupportedGroup object to a SupportedGroupDTO object.

        Args:
            supported_group (SupportedGroup): The SupportedGroup object to map, or None.

        Returns:
            SupportedGroupDTO | None: The mapped SupportedGroupDTO object, or None if the input is None.
        """
        if supported_group is None:
            return None

        supported_group_dto = SupportedGroupDTO()
        supported_group_dto.namespace = supported_group.namespace
        supported_group_dto.cluster = supported_group.cluster
        supported_group_dto.test_files = supported_group.test_files
        supported_group_dto.url = supported_group.url
        supported_group_dto.ms_list = [supported_group.services_data.get_item(service)
                                       for service in supported_group.services_data]
        supported_group_dto.project = supported_group.project
        return supported_group_dto
