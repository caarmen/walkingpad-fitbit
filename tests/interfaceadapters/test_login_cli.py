from typing import Callable

import pytest

from tests.fixtures.authlib import AuthLibScenario
from walkingpadfitbit.auth.usecases import storage
from walkingpadfitbit.interfaceadapters.cli.logincli import login_cli


@pytest.mark.asyncio
async def test_login_cli(
    monkeypatch: pytest.MonkeyPatch,
    fake_oauth_client: Callable[[pytest.MonkeyPatch, AuthLibScenario], None],
):
    """
    Given an authlib setup to provide successful responses,
    When we call the login_cli() api to log in
    Then the call is successful
    And the oauth token is saved.
    """
    with monkeypatch.context() as mp:

        # Given an authlib setup to provide successful responses,
        scenario = AuthLibScenario(
            fake_callback_url="https://someapp.com/callack?a=1&b=2",
            fake_oauth_token={
                "access_token": "some access token",
                "expires_at": 1720908387,
                "refresh_token": "some refresh token",
                "user_id": "some user id",
            },
        )
        fake_oauth_client(
            mp,
            scenario,
        )

        # Simulate the user pasting the callback url.
        mp.setattr("builtins.input", lambda _: scenario.fake_callback_url)

        # When we call the login_cli() api to log in
        await login_cli("some client id", "some client secret")

        # Verify the saved oauth token has the expected values.
        saved_token = storage.read_oauth_token()

        # Then the call is successful
        # And the oauth token is saved.
        assert saved_token["access_token"] == "some access token"
        assert saved_token["expires_at"] == 1720908387
        assert saved_token["refresh_token"] == "some refresh token"
        assert saved_token["user_id"] == "some user id"
