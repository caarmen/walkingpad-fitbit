from typing import Callable

import pytest

from tests.fixtures.authlib import AuthLibMocks, AuthLibScenario
from walkingpadfitbit.auth import storage
from walkingpadfitbit.auth.login import login


@pytest.mark.asyncio
async def test_oauth_login_success(
    monkeypatch: pytest.MonkeyPatch,
    fake_oauth_client: Callable[[pytest.MonkeyPatch, AuthLibScenario], AuthLibMocks],
):
    """
    Given an authlib setup to provide successful responses,
    When we call the login api,
    Then the call succeeds,
    And an oauth token is saved with expected values.
    """
    with monkeypatch.context() as mp:

        # Given an authlib setup to provide successful responses,
        scenario = AuthLibScenario(
            fake_authorization_url="https://fake.fitbit.com/authorize?foo=bar",
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

        # When we call the login api,
        # Step 1 of the login flow: get the auth url.
        login_flow = login(
            client_id="some client id",
            client_secret="some client secret",
        )
        actual_authorization_url = await anext(login_flow)
        assert actual_authorization_url == scenario.fake_authorization_url

        # Step 2 of the login flow: send the callback url
        await login_flow.asend(scenario.fake_callback_url)

        # Then the call succeeds,
        # And an oauth token is saved with expected values.

        # Verify the saved oauth token has the expected values.
        saved_token = storage.read_oauth_token()
        assert saved_token["access_token"] == "some access token"
        assert saved_token["expires_at"] == 1720908387
        assert saved_token["refresh_token"] == "some refresh token"
        assert saved_token["user_id"] == "some user id"
