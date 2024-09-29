from walkingpadfitbit.domain.display.base import BaseDisplay
from walkingpadfitbit.domain.display.formatter import (
    format_distance,
    format_duration,
    format_speed,
)
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


class RichTextDisplay(BaseDisplay):
    def walk_event_to_text(
        self,
        event: TreadmillWalkEvent,
    ) -> str:
        return f"""{chr(27)}[2J{chr(27)}[H{format_distance(event)}
{format_duration(event)}
{format_speed(event)}"""

    def stop_event_to_text(self) -> str:
        return f"""{chr(27)}[2J{chr(27)}[HDistance: --
Duration: --
Speed: --"""
