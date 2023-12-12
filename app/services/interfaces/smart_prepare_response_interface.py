from abc import ABC, abstractmethod

from app.models.group_data import GroupData
from app.models.service_data import ServiceData
from app.models.smart_analyze_response import SmartAnalyzeResponse


class IPrepareResponseStrategy(ABC):
    @abstractmethod
    def get(self, groups_data: dict[str, GroupData], services_data: dict[str, ServiceData]) -> SmartAnalyzeResponse:
        pass
