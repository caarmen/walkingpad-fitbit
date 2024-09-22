from dataclasses import dataclass
from typing import Union


@dataclass
class TreadmillWalkEvent:
    time_s: int
    dist_km: float
    speed_kph: float


TreadmillStopEvent = object()

TreadmillEvent = Union[TreadmillStopEvent, TreadmillWalkEvent]
