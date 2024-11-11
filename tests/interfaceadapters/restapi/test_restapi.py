import dataclasses
import http
from typing import Any

import pytest
from flask.testing import FlaskClient
from pytest import MonkeyPatch
from werkzeug.test import TestResponse

from tests.fakes.ph4_walkingpad.config import configure_fake_walkingpad
from tests.fakes.ph4_walkingpad.fakescanner import ScannerScenario
from walkingpadfitbit import container


@dataclasses.dataclass
class Scenario:
    id: str
    route: str
    expected_status_code: int
    expected_body: dict[str, Any] | None = None


SCENARIOS = [
    Scenario(
        id="start",
        route="start",
        expected_status_code=http.HTTPStatus.NO_CONTENT,
    ),
    Scenario(
        id="stop",
        route="stop",
        expected_status_code=http.HTTPStatus.NO_CONTENT,
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
        )

        container.config.set("device.name", "some device")
        response: TestResponse = restapi_client.post(f"/treadmill/{scenario.route}")
        assert response.status_code == scenario.expected_status_code
        assert response.json == scenario.expected_body
