import signal
import sys
from asyncio import TaskGroup, sleep
from typing import Callable

import pytest

from tests.fakes.ph4_walkingpad.config import configure_fake_walkingpad
from tests.fixtures.authlib import AuthLibMocks, AuthLibScenario
from walkingpadfitbit.auth import storage
from walkingpadfitbit.main import main

fake_oauth_token = {
    "access_token": "some access token",
    "expires_at": 1720908387,
    "refresh_token": "some refresh token",
    "user_id": "some user id",
}


@pytest.fixture
def server_port(
    worker_id: str,  # ex: gw0, gw1, ...
):
    """
    To avoid conflicts running the rest server on the same port when running
    tests in parallel (with -n auto):
    Choose a port starting from 5000, depending on the current test worker.
    """
    base_port = 5000
    if worker_id == "master":
        return base_port

    port_offset = int(worker_id.replace("gw", ""))  # ex: 0, 1, ...

    return base_port + port_offset


@pytest.mark.asyncio
async def test_main_required_args(
    monkeypatch: pytest.MonkeyPatch,
    fake_oauth_client: Callable[[pytest.MonkeyPatch, AuthLibScenario], AuthLibMocks],
    server_port: int,
):
    """
    Given an authlib setup to provide successful responses,
    and no prior oauth token saved,
    And no connected walkingpad
    When we call the main() entry point with required command-line arguments
    Then the authentication is successful
    And the oauth token is saved.
    """
    with monkeypatch.context() as mp:

        # Given an authlib setup to provide successful responses,
        scenario = AuthLibScenario(fake_oauth_token=fake_oauth_token)
        fake_oauth_client(mp, scenario)

        # Given no connected walkingpad
        configure_fake_walkingpad(mp)

        # Simulate the user's command-line arguments.
        mp.setattr(
            sys,
            "argv",
            [
                "main.py",
                "--server-port",
                str(server_port),
                "some device name",
            ],
        )
        # Simulate the user pasting the callback url.
        mp.setattr("builtins.input", lambda _: scenario.fake_callback_url)

        # and no prior oauth token saved,
        saved_token = storage.read_oauth_token()
        assert saved_token is None

        async def send_interrupt_signal():
            await sleep(3)
            signal.raise_signal(signal.SIGINT)

        # When we call the main() entry point
        async with TaskGroup() as tg:
            tg.create_task(main(env_file=".env.test"))
            tg.create_task(send_interrupt_signal())

        # Then the authentication is successful
        # And the oauth token is saved.
        saved_token = storage.read_oauth_token()
        assert saved_token is not None


@pytest.mark.asyncio
async def test_main_optional_args(
    monkeypatch: pytest.MonkeyPatch,
    fake_oauth_client: Callable[[pytest.MonkeyPatch, AuthLibScenario], AuthLibMocks],
    server_port: int,
):
    """
    Given an authlib setup to provide successful responses,
    and no prior oauth token saved,
    And no connected walkingpad
    When we call the main() entry point with optional command-line arguments
    Then the authentication is successful
    And the oauth token is saved.
    """
    with monkeypatch.context() as mp:

        # Given an authlib setup to provide successful responses,
        scenario = AuthLibScenario(fake_oauth_token=fake_oauth_token)
        fake_oauth_client(mp, scenario)

        # Given no connected walkingpad
        configure_fake_walkingpad(mp)

        # Simulate the user's command-line arguments.
        mp.setattr(
            sys,
            "argv",
            [
                "main.py",
                "--monitor-duration",
                "1.0",
                "--poll-interval",
                "0.1",
                "--server-port",
                str(server_port),
                "some device name",
            ],
        )
        # Simulate the user pasting the callback url.
        mp.setattr("builtins.input", lambda _: scenario.fake_callback_url)

        # and no prior oauth token saved,
        saved_token = storage.read_oauth_token()
        assert saved_token is None

        # When we call the main() entry point
        await main(env_file=".env.test")

        # Then the authentication is successful
        # And the oauth token is saved.
        saved_token = storage.read_oauth_token()
        assert saved_token is not None
