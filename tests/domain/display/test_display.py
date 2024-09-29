import pytest

from walkingpadfitbit.domain.display.json import JsonDisplay
from walkingpadfitbit.domain.display.plaintext import PlainTextDisplay
from walkingpadfitbit.domain.display.richtext import RichTextDisplay
from walkingpadfitbit.domain.entities.dailysummary import DailySummary
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


@pytest.mark.parametrize(
    argnames=[
        "event",
        "daily_summary",
        "expected_plaintext_display",
        "expected_richtext_display",
        "expected_json_display",
    ],
    argvalues=[
        (
            TreadmillWalkEvent(
                time_s=60,
                dist_km=0.1,
                speed_kph=2.4,
            ),
            None,
            "Distance: 0.10 km. Duration: 1m. Speed: 2.4 km/h. Total distance: --. Total duration: --.",
            f"{chr(27)}[2J{chr(27)}[HDistance: 0.10 km\nDuration: 1m\nSpeed: 2.4 km/h\nTotal distance: --\nTotal duration: --",
            '{"distance_m": 100, "duration_s": 60, "speed_kph": 2.4, "total_distance_m": null, "total_duration_s": null}',
        ),
        (
            TreadmillWalkEvent(
                time_s=60,
                dist_km=0.1,
                speed_kph=2.4,
            ),
            DailySummary(),
            "Distance: 0.10 km. Duration: 1m. Speed: 2.4 km/h. Total distance: 0.10 km. Total duration: 1m.",
            f"{chr(27)}[2J{chr(27)}[HDistance: 0.10 km\nDuration: 1m\nSpeed: 2.4 km/h\nTotal distance: 0.10 km\nTotal duration: 1m",
            '{"distance_m": 100, "duration_s": 60, "speed_kph": 2.4, "total_distance_m": 100, "total_duration_s": 60}',
        ),
        (
            TreadmillWalkEvent(
                time_s=60,
                dist_km=0.1,
                speed_kph=2.4,
            ),
            DailySummary(
                total_distance_km=4.23,
                total_duration_ms=3540000,
            ),
            "Distance: 0.10 km. Duration: 1m. Speed: 2.4 km/h. Total distance: 4.33 km. Total duration: 1h 0m.",
            f"{chr(27)}[2J{chr(27)}[HDistance: 0.10 km\nDuration: 1m\nSpeed: 2.4 km/h\nTotal distance: 4.33 km\nTotal duration: 1h 0m",
            '{"distance_m": 100, "duration_s": 60, "speed_kph": 2.4, "total_distance_m": 4330, "total_duration_s": 3600}',
        ),
        (
            TreadmillWalkEvent(
                time_s=100000,
                dist_km=0.123456,
                speed_kph=2.456789,
            ),
            DailySummary(),
            "Distance: 0.12 km. Duration: 27h 46m. Speed: 2.5 km/h. Total distance: 0.12 km. Total duration: 27h 46m.",
            f"{chr(27)}[2J{chr(27)}[HDistance: 0.12 km\nDuration: 27h 46m\nSpeed: 2.5 km/h\nTotal distance: 0.12 km\nTotal duration: 27h 46m",
            '{"distance_m": 123, "duration_s": 100000, "speed_kph": 2.5, "total_distance_m": 123, "total_duration_s": 100000}',
        ),
    ],
)
def test_display(
    event: TreadmillWalkEvent,
    daily_summary: DailySummary,
    expected_plaintext_display: str,
    expected_richtext_display: str,
    expected_json_display: str,
):
    assert (
        PlainTextDisplay().walk_event_to_text(
            event=event,
            daily_summary=daily_summary,
        )
        == expected_plaintext_display
    )
    assert (
        RichTextDisplay().walk_event_to_text(
            event=event,
            daily_summary=daily_summary,
        )
        == expected_richtext_display
    )
    assert (
        JsonDisplay().walk_event_to_text(
            event=event,
            daily_summary=daily_summary,
        )
        == expected_json_display
    )
