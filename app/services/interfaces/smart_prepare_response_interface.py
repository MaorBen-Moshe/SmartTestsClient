from abc import ABC, abstractmethod

from app.models.groups_data import TestGroupsData
from app.models.services_data import ServicesData
from app.models.smart_analyze_response import SmartAnalyzeResponse


class IPrepareResponseStrategy(ABC):
    @abstractmethod
    def get(self, groups_data: TestGroupsData, services_data: ServicesData) -> SmartAnalyzeResponse:
        """Gets the smart analyze response for the selected mode.

        Args:
            groups_data (TestGroupsData): The test groups data to prepare the response from.
            services_data (ServicesData): The services data to prepare the response from - IGNORED in INFO mode.

        Returns:
            SmartAnalyzeResponse: The smart analyze response for the selected mode.
        """
        pass
