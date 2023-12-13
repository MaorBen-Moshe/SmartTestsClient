from abc import ABC, abstractmethod

from app.models.group_data import GroupData
from app.models.services_data import ServicesData
from app.models.smart_analyze_response import SmartAnalyzeResponse


class IPrepareResponseStrategy(ABC):
    @abstractmethod
    def get(self, groups_data: dict[str, GroupData], services_data: ServicesData) -> SmartAnalyzeResponse:
        pass
