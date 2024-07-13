import datetime as dt
from typing import Callable

import pytest

from tests.fixtures.authlib import AuthLibScenario
from walkingpadfitbit.auth.entities.oauth_token import OAuthToken
from walkingpadfitbit.auth.usecases import storage
from walkingpadfitbit.auth.usecases.login import login


@pytest.mark.asyncio
async def test_oauth_login_success(
    monkeypatch: pytest.MonkeyPatch,
    fake_oauth_client: Callable[[pytest.MonkeyPatch, AuthLibScenario], None],
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
                "expires_at": "2024-07-13T22:06:27Z",
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

        # Steps 2-3 of the login flow: send the callback url and get the oauth token.
        returned_token: OAuthToken = await login_flow.asend(scenario.fake_callback_url)

        # Then the call succeeds,
        # And an oauth token is saved with expected values.

        # Verify the returned oauth token has the expected values.
        assert returned_token.access_token == "some access token"
        assert returned_token.expires_at == dt.datetime(
            2024, 7, 13, 22, 6, 27, tzinfo=dt.timezone.utc
        )
        assert returned_token.refresh_token == "some refresh token"
        assert returned_token.user_id == "some user id"

        # Verify the returned oauth token was saved.
        saved_token = storage.read_oauth_token()
        assert returned_token == saved_token
