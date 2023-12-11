from abc import ABC, abstractmethod

from app.models.analyze_app_params import AnalyzeAppServiceParameters


class SmartAnalyzeStepInterface(ABC):
    @abstractmethod
    def execute(self, parameters: AnalyzeAppServiceParameters):
        pass
