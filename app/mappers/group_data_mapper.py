from __future__ import annotations

from app.models.dto.group_data_dto import GroupDataDTO
from app.models.group_data import GroupData


class GroupDataMapper:
    """A class that maps a GroupData instance to a GroupDataDTO instance."""

    @classmethod
    def map_to_dto(cls, group_data: GroupData) -> GroupDataDTO | None:
        """Maps a GroupData instance to a GroupDataDTO instance.

        Args:
            group_data (GroupData): The GroupData instance to map, or None.

        Returns:
            GroupDataDTO | None: The mapped GroupDataDTO instance, or None if the input is None.
        """
        if group_data is None:
            return None

        group_data_dto = GroupDataDTO()
        group_data_dto.test_xml_name = group_data.test_xml_name
        group_data_dto.test_xml_path = group_data.test_xml_path
        group_data_dto.total_flows_count = group_data.total_flows_count
        group_data_dto.curr_flows_count = group_data.curr_flows_count
        group_data_dto.flows = group_data.flows

        return group_data_dto
