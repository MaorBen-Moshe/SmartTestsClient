from abc import ABC, abstractmethod

from app.models.groups_data import TestGroupsData
from app.models.services_data import ServicesData
from app.models.smart_analyze_response import SmartAnalyzeResponse


class IPrepareResponseStrategy(ABC):
    @abstractmethod
    def get(self, groups_data: TestGroupsData, services_data: ServicesData) -> SmartAnalyzeResponse:
        pass
