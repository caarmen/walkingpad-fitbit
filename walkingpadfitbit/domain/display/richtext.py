from walkingpadfitbit.domain.display.base import BaseDisplay
from walkingpadfitbit.domain.display.formatter import (
    format_distance,
    format_duration,
    format_speed,
    format_total_distance,
    format_total_duration,
)
from walkingpadfitbit.domain.entities.dailysummary import DailySummary
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


class RichTextDisplay(BaseDisplay):
    def walk_event_to_text(
        self,
        event: TreadmillWalkEvent,
        daily_summary: DailySummary | None,
    ) -> str:
        return f"""{chr(27)}[2J{chr(27)}[H{format_distance(event)}
{format_duration(event)}
{format_speed(event)}
{format_total_distance(event, daily_summary)}
{format_total_duration(event, daily_summary)}"""

    def stop_event_to_text(
        self,
        last_event: TreadmillWalkEvent,
        daily_summary: DailySummary | None,
    ) -> str:
        return f"""{chr(27)}[2J{chr(27)}[HDistance: --
Duration: --
Speed: --
{format_total_distance(last_event, daily_summary)}
{format_total_duration(last_event, daily_summary)}"""
