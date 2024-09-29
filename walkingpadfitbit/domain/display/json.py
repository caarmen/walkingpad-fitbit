import json

from walkingpadfitbit.domain.display.base import BaseDisplay
from walkingpadfitbit.domain.entities.dailysummary import DailySummary
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


class JsonDisplay(BaseDisplay):
    def walk_event_to_text(
        self,
        event: TreadmillWalkEvent,
        daily_summary: DailySummary | None,
    ) -> str:
        return json.dumps(
            {
                "distance_m": int(event.dist_km * 1000),
                "duration_s": event.time_s,
                "speed_kph": round(event.speed_kph, 1),
                "total_distance_m": (
                    int((event.dist_km + daily_summary.total_distance_km) * 1000)
                    if daily_summary
                    else None
                ),
                "total_duration_s": (
                    (event.time_s + (daily_summary.total_duration_ms // 1000))
                    if daily_summary
                    else None
                ),
            }
        )

    def stop_event_to_text(
        self,
        last_event: TreadmillWalkEvent,
        daily_summary: DailySummary | None,
    ) -> str:
        return json.dumps(
            {
                "distance_m": None,
                "duration_s": None,
                "speed_kph": None,
                "total_distance_m": (
                    int((last_event.dist_km + daily_summary.total_distance_km) * 1000)
                    if daily_summary
                    else None
                ),
                "total_duration_s": (
                    (last_event.time_s + (daily_summary.total_duration_ms // 1000))
                    if daily_summary
                    else None
                ),
            }
        )
