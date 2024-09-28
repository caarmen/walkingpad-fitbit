import datetime as dt
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Callable
from zoneinfo import ZoneInfo

import pytest
from bleak.exc import BleakDeviceNotFoundError

from tests.fakes.builtins.fakestdout import FakeStdout
from tests.fakes.ph4_walkingpad.config import configure_fake_walkingpad
from tests.fakes.ph4_walkingpad.fakecontroller import (
    ControllerScenario,
    FakeWalkingPadCurStatus,
)
from tests.fakes.ph4_walkingpad.fakescanner import ScannerScenario
from tests.fixtures.authlib import AuthLibMocks, AuthLibScenario
from walkingpadfitbit.domain.display.factory import DisplayMode, get_display
from walkingpadfitbit.domain.eventhandler import TreadmillEventHandler
from walkingpadfitbit.domain.eventhandler import dt as datetime_to_freeze
from walkingpadfitbit.domain.remoterepository import RemoteActivityRepository
from walkingpadfitbit.interfaceadapters.walkingpad.monitor import monitor


@dataclass
class MonitorScenario:
    id: str
    fake_walking_pad_cur_statuses: list[FakeWalkingPadCurStatus]
    expected_output_text: dict[DisplayMode, str]
    expected_post_call_count: int
    expected_post_query_params: dict[str, int | float | str] | None = None


MONITOR_DURATION_ELAPSED_SCENARIOS = [
    MonitorScenario(
        id="one walk, one stop",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1200,
                speed=20,
            ),
            FakeWalkingPadCurStatus(
                belt_state=0,
                dist=0,
                time=0,
                speed=0,
            ),
        ],
        expected_post_call_count=1,
        expected_post_query_params={
            "date": "2038-04-01",
            "startTime": "04:13",
            "durationMillis": 1200000,
            "distance": pytest.approx(1.253),
            "activityId": 90019,
            "distanceUnit": "Kilometer",
            "manualCalories": 0,
        },
        expected_output_text={
            DisplayMode.PLAIN_TEXT: """Distance: 1.25 km. Duration: 20m. Speed: 2.0 km/h.
Distance: --. Duration: --. Speed: --.
""",
            DisplayMode.JSON: """{"distance_m": 1253, "duration_s": 1200, "speed_kph": 2.0}
{"distance_m": null, "duration_s": null, "speed_kph": null}
""",
            DisplayMode.RICH_TEXT: f"""{chr(27)}[2J{chr(27)}[HDistance: 1.25 km
Duration: 20m
Speed: 2.0 km/h
{chr(27)}[2J{chr(27)}[HDistance: --
Duration: --
Speed: --
""",
        },
    ),
    MonitorScenario(
        id="no events",
        fake_walking_pad_cur_statuses=[],
        expected_post_call_count=0,
        expected_output_text={
            DisplayMode.PLAIN_TEXT: "",
            DisplayMode.JSON: "",
            DisplayMode.RICH_TEXT: "",
        },
    ),
    MonitorScenario(
        id="two walk events",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1200,
                speed=20,
            ),
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1201,
                speed=21,
            ),
        ],
        expected_post_call_count=1,
        expected_post_query_params={
            "date": "2038-04-01",
            "startTime": "04:13",
            "durationMillis": 1201000,
            "distance": pytest.approx(1.253),
            "activityId": 90019,
            "distanceUnit": "Kilometer",
            "manualCalories": 0,
        },
        expected_output_text={
            DisplayMode.PLAIN_TEXT: """Distance: 1.25 km. Duration: 20m. Speed: 2.0 km/h.
Distance: 1.25 km. Duration: 20m. Speed: 2.1 km/h.
Distance: --. Duration: --. Speed: --.
""",
            DisplayMode.JSON: """{"distance_m": 1253, "duration_s": 1200, "speed_kph": 2.0}
{"distance_m": 1253, "duration_s": 1201, "speed_kph": 2.1}
{"distance_m": null, "duration_s": null, "speed_kph": null}
""",
            DisplayMode.RICH_TEXT: f"""{chr(27)}[2J{chr(27)}[HDistance: 1.25 km
Duration: 20m
Speed: 2.0 km/h
{chr(27)}[2J{chr(27)}[HDistance: 1.25 km
Duration: 20m
Speed: 2.1 km/h
{chr(27)}[2J{chr(27)}[HDistance: --
Duration: --
Speed: --
""",
        },
    ),
    MonitorScenario(
        id="two stop events",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=0,
                dist=0,
                time=0,
                speed=0,
            ),
            FakeWalkingPadCurStatus(
                belt_state=0,
                dist=0,
                time=0,
                speed=0,
            ),
        ],
        expected_post_call_count=0,
        expected_output_text={
            DisplayMode.PLAIN_TEXT: "",
            DisplayMode.JSON: "",
            DisplayMode.RICH_TEXT: "",
        },
    ),
    MonitorScenario(
        id="one walk, one unknown",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1201,
                speed=20,
            ),
            FakeWalkingPadCurStatus(
                belt_state=7,
                dist=0,
                time=0,
                speed=0,
            ),
        ],
        expected_post_call_count=1,
        expected_post_query_params={
            "date": "2038-04-01",
            "startTime": "04:13",
            "durationMillis": 1201000,
            "distance": pytest.approx(1.253),
            "activityId": 90019,
            "distanceUnit": "Kilometer",
            "manualCalories": 0,
        },
        expected_output_text={
            DisplayMode.PLAIN_TEXT: """Distance: 1.25 km. Duration: 20m. Speed: 2.0 km/h.
Distance: --. Duration: --. Speed: --.
""",
            DisplayMode.JSON: """{"distance_m": 1253, "duration_s": 1201, "speed_kph": 2.0}
{"distance_m": null, "duration_s": null, "speed_kph": null}
""",
            DisplayMode.RICH_TEXT: f"""{chr(27)}[2J{chr(27)}[HDistance: 1.25 km
Duration: 20m
Speed: 2.0 km/h
{chr(27)}[2J{chr(27)}[HDistance: --
Duration: --
Speed: --
""",
        },
    ),
    MonitorScenario(
        id="one stop, one walk",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=0,
                dist=0,
                time=0,
                speed=0,
            ),
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1201,
                speed=20,
            ),
        ],
        expected_post_call_count=1,
        expected_post_query_params={
            "date": "2038-04-01",
            "startTime": "04:13",
            "durationMillis": 1201000,
            "distance": pytest.approx(1.253),
            "activityId": 90019,
            "distanceUnit": "Kilometer",
            "manualCalories": 0,
        },
        expected_output_text={
            DisplayMode.PLAIN_TEXT: """Distance: 1.25 km. Duration: 20m. Speed: 2.0 km/h.
Distance: --. Duration: --. Speed: --.
""",
            DisplayMode.JSON: """{"distance_m": 1253, "duration_s": 1201, "speed_kph": 2.0}
{"distance_m": null, "duration_s": null, "speed_kph": null}
""",
            DisplayMode.RICH_TEXT: f"""{chr(27)}[2J{chr(27)}[HDistance: 1.25 km
Duration: 20m
Speed: 2.0 km/h
{chr(27)}[2J{chr(27)}[HDistance: --
Duration: --
Speed: --
""",
        },
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    argnames="display_mode",
    argvalues=[
        DisplayMode.PLAIN_TEXT,
        DisplayMode.JSON,
        DisplayMode.RICH_TEXT,
    ],
)
@pytest.mark.parametrize(
    ids=[
        "no exception",
        "reconnect timeout",
        "bleak exception",
        "unexpected error",
    ],
    argnames="controller_run_exceptions",
    argvalues=[
        None,
        [None, TimeoutError],
        [None, BleakDeviceNotFoundError("my device")],
        [None, ValueError("omg")],
    ],
)
@pytest.mark.parametrize(
    ids=["connected", "disconnected"],
    argnames="is_connected_values",
    argvalues=[
        [True, True, True],
        [True, False, True],
    ],
)
@pytest.mark.parametrize(
    ids=[x.id for x in MONITOR_DURATION_ELAPSED_SCENARIOS],
    argnames=["monitor_scenario"],
    argvalues=[[x] for x in MONITOR_DURATION_ELAPSED_SCENARIOS],
)
async def test_monitor_monitoring_duration_elapsed(
    monkeypatch: pytest.MonkeyPatch,
    display_mode: DisplayMode,
    event_output: FakeStdout,
    remote_activity_repository: RemoteActivityRepository,
    freeze_time: Callable[
        [pytest.MonkeyPatch, ModuleType, tuple[Any], dt.timezone], None
    ],
    fake_oauth_client: Callable[[pytest.MonkeyPatch, AuthLibScenario], AuthLibMocks],
    monitor_scenario: MonitorScenario,
    is_connected_values: list[bool],
    controller_run_exceptions: list[Exception],
):
    """
    Given a scenario where the walking pad emits certain data
    When we monitor the walking pad data until the monitoring duration elapses
    Then we send the expected api calls to Fitbit to log (or not) the activity.
    And we output the expected text to the screen.
    """
    treadmill_event_handler = TreadmillEventHandler(
        remote_activity_repository=remote_activity_repository,
        display=get_display(display_mode),
        event_output=event_output,
    )
    with monkeypatch.context() as mp:

        # Given a scenario where the walking pad emits certain data
        freeze_time(
            mp,
            datetime_to_freeze,
            frozen_datetime_args=(2038, 4, 1, 11, 33, 44, 0),
            local_timezone=ZoneInfo("America/Los_Angeles"),
        )
        authlib_mocks: AuthLibMocks = fake_oauth_client(mp, AuthLibScenario())
        configure_fake_walkingpad(
            mp,
            ScannerScenario(
                found_addresses=["some address"],
            ),
            ControllerScenario(
                cur_statuses=monitor_scenario.fake_walking_pad_cur_statuses,
                is_connected_values=is_connected_values,
                run_exceptions=controller_run_exceptions,
            ),
        )

        # When we monitor the walking pad data
        await monitor(
            device_name="some device",
            treadmill_event_handler=treadmill_event_handler,
            monitor_duration_s=1.0,
            poll_interval_s=0.1,
        )

        # Then we send the expected api calls to Fitbit to log (or not) the activity.
        assert (
            authlib_mocks.post.call_count == monitor_scenario.expected_post_call_count
        )
        if monitor_scenario.expected_post_call_count:
            actual_query_params = authlib_mocks.post.call_args[1]["params"]
            assert actual_query_params == monitor_scenario.expected_post_query_params

        # And we output the expected text to the screen.
        actual_lines_written = event_output.lines_written
        assert (
            actual_lines_written == monitor_scenario.expected_output_text[display_mode]
        )