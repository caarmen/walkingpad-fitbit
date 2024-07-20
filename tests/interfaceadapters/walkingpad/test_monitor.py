import datetime as dt
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Callable
from zoneinfo import ZoneInfo

import pytest

from tests.fixtures.authlib import AuthLibMocks, AuthLibScenario
from tests.fixtures.ph4_walkingpad import FakeWalkingPadCurStatus, WalkingPadScenario
from walkingpadfitbit.domain.eventhandler import TreadmillEventHandler
from walkingpadfitbit.domain.eventhandler import dt as datetime_to_freeze
from walkingpadfitbit.interfaceadapters.walkingpad.monitor import monitor


@dataclass
class MonitorScenario:
    id: str
    fake_walking_pad_cur_statuses: list[FakeWalkingPadCurStatus]
    expected_post_call_count: int
    expected_post_query_params: dict[str, int | float | str] | None = None


MONITOR_SCENARIOS = [
    MonitorScenario(
        id="one walk, one stop",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1200,
            ),
            FakeWalkingPadCurStatus(
                belt_state=0,
                dist=0,
                time=0,
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
        },
    ),
    MonitorScenario(
        id="no events",
        fake_walking_pad_cur_statuses=[],
        expected_post_call_count=0,
    ),
    MonitorScenario(
        id="two walk events",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1200,
            ),
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1201,
            ),
        ],
        expected_post_call_count=0,
    ),
    MonitorScenario(
        id="two stop events",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=0,
                dist=0,
                time=0,
            ),
            FakeWalkingPadCurStatus(
                belt_state=0,
                dist=0,
                time=0,
            ),
        ],
        expected_post_call_count=0,
    ),
    MonitorScenario(
        id="one walk, one unknown",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1201,
            ),
            FakeWalkingPadCurStatus(
                belt_state=7,
                dist=0,
                time=0,
            ),
        ],
        expected_post_call_count=0,
    ),
    MonitorScenario(
        id="one stop, one walk",
        fake_walking_pad_cur_statuses=[
            FakeWalkingPadCurStatus(
                belt_state=0,
                dist=0,
                time=0,
            ),
            FakeWalkingPadCurStatus(
                belt_state=1,
                dist=125.3,
                time=1201,
            ),
        ],
        expected_post_call_count=0,
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ids=[x.id for x in MONITOR_SCENARIOS],
    argnames=["monitor_scenario"],
    argvalues=[[x] for x in MONITOR_SCENARIOS],
)
async def test_monitor(
    monkeypatch: pytest.MonkeyPatch,
    treadmill_event_handler: TreadmillEventHandler,
    freeze_time: Callable[
        [pytest.MonkeyPatch, ModuleType, tuple[Any], dt.timezone], None
    ],
    fake_oauth_client: Callable[[pytest.MonkeyPatch, AuthLibScenario], AuthLibMocks],
    fake_walking_pad: Callable[[pytest.MonkeyPatch, WalkingPadScenario], None],
    monitor_scenario: MonitorScenario,
):
    """
    Given a scenario where the walking pad emits certain data
    When we monitor the walking pad data
    Then we send the expected api calls to Fitbit to log (or not) the activity.
    """
    with monkeypatch.context() as mp:

        # Given a scenario where the walking pad emits certain data
        freeze_time(
            mp,
            datetime_to_freeze,
            frozen_datetime_args=(2038, 4, 1, 11, 33, 44, 0),
            local_timezone=ZoneInfo("America/Los_Angeles"),
        )
        authlib_mocks: AuthLibMocks = fake_oauth_client(mp, AuthLibScenario())
        fake_walking_pad(
            mp,
            WalkingPadScenario(
                found_addresses=["some address"],
                cur_statuses=monitor_scenario.fake_walking_pad_cur_statuses,
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
