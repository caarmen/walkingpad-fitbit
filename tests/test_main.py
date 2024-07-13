from typing import Callable

import pytest

from tests.fixtures.authlib import AuthLibScenario
from walkingpadfitbit.auth.usecases import storage
from walkingpadfitbit.main import main


@pytest.mark.asyncio
async def test_main(
    monkeypatch: pytest.MonkeyPatch,
    fake_oauth_client: Callable[[pytest.MonkeyPatch, AuthLibScenario], None],
):
    """
    Given an authlib setup to provide successful responses,
    and no prior oauth token saved,
    When we call the main() entry point
    Then the authentication is successful
    And the oauth token is saved.
    """
    with monkeypatch.context() as mp:

        # Given an authlib setup to provide successful responses,
        scenario = AuthLibScenario(
            fake_oauth_token={
                "access_token": "some access token",
                "expires_at": 1720908387,
                "refresh_token": "some refresh token",
                "user_id": "some user id",
            },
        )
        fake_oauth_client(mp, scenario)

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
