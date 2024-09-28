from walkingpadfitbit.domain.display.base import BaseDisplay
from walkingpadfitbit.domain.display.duration import friendly_duration
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


class PlainTextDisplay(BaseDisplay):
    def walk_event_to_text(
        self,
        event: TreadmillWalkEvent,
    ) -> str:
        return f"Distance: {event.dist_km:.2f} km. Duration: {friendly_duration(event.time_s)}. Speed: {event.speed_kph:.1f} km/h."

    def stop_event_to_text(self) -> str:
        return "Distance: --. Duration: --. Speed: --."
