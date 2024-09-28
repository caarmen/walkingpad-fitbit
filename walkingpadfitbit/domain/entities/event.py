from dataclasses import dataclass
from typing import Union


@dataclass
class TreadmillWalkEvent:
    time_s: int
    dist_km: float


class TreadmillStopEvent: ...


TreadmillEvent = Union[TreadmillStopEvent, TreadmillWalkEvent]
