from __future__ import annotations

from abc import abstractmethod, ABC

from app.services.interfaces.smart_prepare_response_interface import IPrepareResponseStrategy


class IPrepareResponseStrategyFactory(ABC):
    @abstractmethod
    def get(self, info_level: str | None) -> IPrepareResponseStrategy:
        pass
