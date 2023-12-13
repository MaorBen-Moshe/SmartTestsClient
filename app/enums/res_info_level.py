from enum import Enum


class ResInfoLevelEnum(Enum):
    INFO = 1
    DEBUG = 2

    @classmethod
    def get_level(cls, level: str):
        return cls[level.upper()] if level and level.upper() in cls.__members__ else cls.INFO
