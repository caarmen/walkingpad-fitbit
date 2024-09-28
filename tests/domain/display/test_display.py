import pytest

from walkingpadfitbit.domain.display.json import JsonDisplay
from walkingpadfitbit.domain.display.plaintext import PlainTextDisplay
from walkingpadfitbit.domain.display.richtext import RichTextDisplay
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


@pytest.mark.parametrize(
    argnames=[
        "event",
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
            "Distance: 0.10 km. Duration: 1m. Speed: 2.4 km/h.",
            f"{chr(27)}[2J{chr(27)}[HDistance: 0.10 km\nDuration: 1m\nSpeed: 2.4 km/h",
            '{"distance_m": 100, "duration_s": 60, "speed_kph": 2.4}',
        ),
        (
            TreadmillWalkEvent(
                time_s=100000,
                dist_km=0.123456,
                speed_kph=2.456789,
            ),
            "Distance: 0.12 km. Duration: 27h 46m. Speed: 2.5 km/h.",
            f"{chr(27)}[2J{chr(27)}[HDistance: 0.12 km\nDuration: 27h 46m\nSpeed: 2.5 km/h",
            '{"distance_m": 123, "duration_s": 100000, "speed_kph": 2.5}',
        ),
    ],
)
def test_display(
    event: TreadmillWalkEvent,
    expected_plaintext_display: str,
    expected_richtext_display: str,
    expected_json_display: str,
):
    assert PlainTextDisplay().walk_event_to_text(event) == expected_plaintext_display
    assert RichTextDisplay().walk_event_to_text(event) == expected_richtext_display
    assert JsonDisplay().walk_event_to_text(event) == expected_json_display
