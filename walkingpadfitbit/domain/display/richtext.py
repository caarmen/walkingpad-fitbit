from walkingpadfitbit.domain.display.base import BaseDisplay
from walkingpadfitbit.domain.display.duration import friendly_duration
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


class RichTextDisplay(BaseDisplay):
    def walk_event_to_text(
        self,
        event: TreadmillWalkEvent,
    ) -> str:
        return f"""{chr(27)}[2J{chr(27)}[HDistance: {event.dist_km:.2f} km
Duration: {friendly_duration(event.time_s)}
Speed: {event.speed_kph:.1f} km/h"""

    def stop_event_to_text(self) -> str:
        return f"""{chr(27)}[2J{chr(27)}[HDistance: --
Duration: --
Speed: --"""
