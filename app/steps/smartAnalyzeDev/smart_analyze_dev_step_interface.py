from abc import ABC, abstractmethod

from app.models.analyze_dev_app_params import AnalyzeDevAppServiceParameters


class SmartAnalyzeDevStepInterface(ABC):
    @abstractmethod
    def execute(self, parameters: AnalyzeDevAppServiceParameters):
        pass
