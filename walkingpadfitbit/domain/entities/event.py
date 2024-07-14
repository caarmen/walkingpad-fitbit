from dataclasses import dataclass
from typing import Union


@dataclass
class TreadmillWalkEvent:
    time_s: int
    dist_km: float


TreadmillStopEvent = object()

TreadmillEvent = Union[TreadmillStopEvent, TreadmillWalkEvent]
