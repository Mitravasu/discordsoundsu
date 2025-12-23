from dataclasses import dataclass
from datetime import time
from zoneinfo import ZoneInfo

@dataclass
class SleepData:
    """
    Represents data for a sleep event
    """
    is_enabled: bool
    time: time
    timezone: ZoneInfo
    sound: str