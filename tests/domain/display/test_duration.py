import pytest

from walkingpadfitbit.domain.display.formatter import friendly_duration


@pytest.mark.parametrize(
    argnames=[
        "duration_s",
        "expected_friendly_duration",
    ],
    argvalues=[
        (59, "0m"),
        (60, "1m"),
        (61, "1m"),
        (119, "1m"),
        (120, "2m"),
        (121, "2m"),
        (3599, "59m"),
        (3600, "1h 0m"),
        (3601, "1h 0m"),
        (3659, "1h 0m"),
        (3660, "1h 1m"),
        (3661, "1h 1m"),
        (86399, "23h 59m"),
        (86400, "24h 0m"),
        (86401, "24h 0m"),
        (86459, "24h 0m"),
        (86460, "24h 1m"),
    ],
)
def test_friendly_duration(duration_s: int, expected_friendly_duration: str):
    actual_friendly_duration = friendly_duration(duration_s)
    assert actual_friendly_duration == expected_friendly_duration
