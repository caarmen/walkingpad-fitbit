import signal
import sys
from asyncio import TaskGroup, sleep
from typing import Callable

import pytest

from tests.fixtures.authlib import AuthLibMocks, AuthLibScenario
from tests.fixtures.ph4_walkingpad import WalkingPadScenario
from walkingpadfitbit.auth import storage
from walkingpadfitbit.main import main

fake_oauth_token = {
    "access_token": "some access token",
    "expires_at": 1720908387,
    "refresh_token": "some refresh token",
    "user_id": "some user id",
}


@pytest.mark.asyncio
async def test_main_required_args(
    monkeypatch: pytest.MonkeyPatch,
    fake_oauth_client: Callable[[pytest.MonkeyPatch, AuthLibScenario], AuthLibMocks],
    fake_walking_pad: Callable[[pytest.MonkeyPatch, WalkingPadScenario], None],
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
        fake_walking_pad(mp, WalkingPadScenario())

        # Simulate the user's command-line arguments.
        mp.setattr(sys, "argv", ["main.py", "some device name"])
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
    fake_walking_pad: Callable[[pytest.MonkeyPatch, WalkingPadScenario], None],
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
        fake_walking_pad(mp, WalkingPadScenario())

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
