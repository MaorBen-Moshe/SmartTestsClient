from __future__ import annotations

from app.enums.res_info_level import ResInfoLevelEnum
from app.services.interfaces.smart_prepare_response_interface import IPrepareResponseStrategy
from app.services.interfaces.smart_prepare_response_strategy_factory_interface import IPrepareResponseStrategyFactory
from app.services.smart_debug_prepare_response import DebugPrepareResponseStrategy
from app.services.smart_info_prepare_response import InfoPrepareResponseStrategy


class PrepareResponseStrategyFactory (IPrepareResponseStrategyFactory):

    def get(self, info_level: ResInfoLevelEnum) -> IPrepareResponseStrategy:
        res = InfoPrepareResponseStrategy()
        if info_level == ResInfoLevelEnum.DEBUG:
            res = DebugPrepareResponseStrategy()
        elif info_level == ResInfoLevelEnum.INFO:
            res = InfoPrepareResponseStrategy()

        return res
