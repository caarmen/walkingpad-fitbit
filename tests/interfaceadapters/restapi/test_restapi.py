import dataclasses
import http
from typing import Any

import pytest
from flask.testing import FlaskClient
from pytest import MonkeyPatch
from werkzeug.test import TestResponse

from tests.fakes.ph4_walkingpad.config import configure_fake_walkingpad
from tests.fakes.ph4_walkingpad.fakecontroller import (
    ControllerScenario,
    FakeWalkingPadCurStatus,
)
from tests.fakes.ph4_walkingpad.fakescanner import ScannerScenario
from walkingpadfitbit import container


@dataclasses.dataclass
class Scenario:
    id: str
    route: str
    request_input: dict[str, Any] | None
    expected_status_code: int
    expected_body: dict[str, Any] | None = None
    controller_scenario: ControllerScenario | None = None


SCENARIOS = [
    Scenario(
        id="start",
        route="start",
        request_input=None,
        expected_status_code=http.HTTPStatus.NO_CONTENT,
    ),
    Scenario(
        id="stop",
        route="stop",
        request_input=None,
        expected_status_code=http.HTTPStatus.NO_CONTENT,
    ),
    Scenario(
        id="toggle started",
        route="toggle-start-stop",
        request_input=None,
        expected_status_code=http.HTTPStatus.OK,
        expected_body={"status": "started"},
    ),
    Scenario(
        id="toggle stopped",
        route="toggle-start-stop",
        request_input=None,
        expected_status_code=http.HTTPStatus.OK,
        expected_body={"status": "stopped"},
        controller_scenario=ControllerScenario(
            last_status=FakeWalkingPadCurStatus(
                dist=10,
                time=5,
                belt_state=1,
                speed=1,
            )
        ),
    ),
    Scenario(
        id="increase speed by 0.5",
        route="change-speed-by",
        request_input={"speed_delta_kph": 0.5},
        expected_status_code=http.HTTPStatus.OK,
        expected_body={"new_speed_kph": pytest.approx(4.5)},
        controller_scenario=ControllerScenario(
            last_status=FakeWalkingPadCurStatus(
                dist=10,
                time=5,
                belt_state=1,
                speed=40,  # 4.0 kph
            )
        ),
    ),
    Scenario(
        id="decrease speed by 0.5",
        route="change-speed-by",
        request_input={"speed_delta_kph": -0.5},
        expected_status_code=http.HTTPStatus.OK,
        expected_body={"new_speed_kph": pytest.approx(3.5)},
        controller_scenario=ControllerScenario(
            last_status=FakeWalkingPadCurStatus(
                dist=10,
                time=5,
                belt_state=1,
                speed=40,  # 4.0 kph
            )
        ),
    ),
    Scenario(
        id="increase speed by too large number",
        route="change-speed-by",
        request_input={"speed_delta_kph": 100.0},
        expected_status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
        expected_body={"code": 422},
        controller_scenario=ControllerScenario(
            last_status=FakeWalkingPadCurStatus(
                dist=10,
                time=5,
                belt_state=1,
                speed=40,  # 4.0 kph
            )
        ),
    ),
    Scenario(
        id="increase speed when no previous speed",
        route="change-speed-by",
        request_input={"speed_delta_kph": 0.8},
        expected_status_code=http.HTTPStatus.OK,
        expected_body={"new_speed_kph": pytest.approx(0.8)},
        controller_scenario=ControllerScenario(),
    ),
    Scenario(
        id="decrease speed to be negative",
        route="change-speed-by",
        request_input={"speed_delta_kph": -1.0},
        expected_status_code=http.HTTPStatus.OK,
        expected_body={"new_speed_kph": 0.0},
        controller_scenario=ControllerScenario(
            last_status=FakeWalkingPadCurStatus(
                dist=10,
                time=5,
                belt_state=1,
                speed=5,  # 0.5 kph
            )
        ),
    ),
]


@pytest.mark.parametrize(
    ids=[x.id for x in SCENARIOS],
    argnames="scenario",
    argvalues=SCENARIOS,
)
def test_treadmill_command(
    restapi_client: FlaskClient,
    monkeypatch: MonkeyPatch,
    scenario: Scenario,
):
    with monkeypatch.context() as mp:
        configure_fake_walkingpad(
            mp,
            ScannerScenario(
                found_addresses=["some address"],
            ),
            controller_scenario=scenario.controller_scenario,
        )

        container.config.set("device.name", "some device")
        response: TestResponse = restapi_client.post(
            f"/treadmill/{scenario.route}",
            json=scenario.request_input,
        )
        assert response.status_code == scenario.expected_status_code
        if scenario.expected_body is None:
            assert response.json is None
        else:
            # Check that the actual response contains at least the content of the expected response.
            # Don't compare the full contents: in the case of errors, the framework adds some detailed error messages
            # for which we don't need to assert the exact content.
            assert response.json.items() >= scenario.expected_body.items()
