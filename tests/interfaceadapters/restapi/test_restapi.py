import http

import pytest
from flask.testing import FlaskClient
from pytest import MonkeyPatch
from werkzeug.test import TestResponse

from tests.fakes.ph4_walkingpad.config import configure_fake_walkingpad
from tests.fakes.ph4_walkingpad.fakescanner import ScannerScenario
from walkingpadfitbit import container


@pytest.mark.parametrize(
    argnames="command",
    argvalues=["start", "stop"],
)
def test_treadmill_command(
    restapi_client: FlaskClient,
    monkeypatch: MonkeyPatch,
    command: str,
):
    with monkeypatch.context() as mp:
        configure_fake_walkingpad(
            mp,
            ScannerScenario(
                found_addresses=["some address"],
            ),
        )

        container.config.set("device.name", "some device")
        response: TestResponse = restapi_client.post(f"/treadmill/{command}")
        assert response.status_code == http.HTTPStatus.NO_CONTENT
