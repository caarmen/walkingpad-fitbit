import json

from walkingpadfitbit.domain.display.base import BaseDisplay
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


class JsonDisplay(BaseDisplay):
    def walk_event_to_text(
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

    def stop_event_to_text(self) -> str:
        return json.dumps(
            {
                "distance_m": None,
                "duration_s": None,
                "speed_kph": None,
            }
        )
