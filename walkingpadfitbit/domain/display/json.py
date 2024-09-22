import json

from walkingpadfitbit.domain.display.base import BaseDisplay
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


class JsonDisplay(BaseDisplay):
    def to_text(
        self,
        event: TreadmillWalkEvent,
    ) -> str:
        return json.dumps(
            {
                "distance_m": int(event.dist_km * 1000),
                "duration_s": event.time_s,
                "speed_kph": round(event.speed_kph, 1),
            }
        )
