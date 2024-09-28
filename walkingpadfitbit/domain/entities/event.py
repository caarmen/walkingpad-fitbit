from dataclasses import dataclass
from typing import Union


@dataclass
class TreadmillWalkEvent:
    time_s: int
    dist_km: float
    speed_kph: float


class TreadmillStopEvent: ...


TreadmillEvent = Union[TreadmillStopEvent, TreadmillWalkEvent]
