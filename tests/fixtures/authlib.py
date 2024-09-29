import uuid
from dataclasses import dataclass
from typing import Any, Callable
from unittest.mock import Mock, create_autospec

import pytest
from authlib.integrations.httpx_client import AsyncOAuth2Client
from httpx import Response


@dataclass
class AuthLibScenario:
    fake_authorization_url: str = "https://fake.fitbit.com/authorize?foo=bar"
    fake_callback_url: str = "https://myapp.com/oauth/fitbit/?abc=def"
    fake_oauth_token: dict[str, Any] | None = None
    fake_get_response: Response = Response(
        status_code=200,
        json={},
    )


@dataclass
class AuthLibMocks:
    create_authorization_url: Mock
    fetch_token: Mock
    post: Mock
    get: Mock


@pytest.fixture
def fake_oauth_client() -> (
    Callable[[pytest.MonkeyPatch, AuthLibScenario], AuthLibMocks]
):
    """
    Use fake replacements for authlib apis.
    """

    def create_fake_oauth_client(
        mp: pytest.MonkeyPatch,
        scenario: AuthLibScenario,
    ):

        # Fake the create_authorization_url() api.
        fake_state = str(uuid.uuid4())

        def fake_create_authorization_url(self, *args, **kwargs):
            return (scenario.fake_authorization_url, fake_state)

        mock_create_authorization_url = create_autospec(
            AsyncOAuth2Client.create_authorization_url,
            side_effect=fake_create_authorization_url,
        )
        mp.setattr(
            AsyncOAuth2Client,
            "create_authorization_url",
            mock_create_authorization_url,
        )

        # Fake the fetch_token() api.
        async def fake_fetch_token(self, *args, **kwargs):
            # Make sure our code passes the expected values as arguments
            # to the authlib api.
            assert (
                kwargs.get("authorization_response", None) == scenario.fake_callback_url
            )
            assert self.state == fake_state
            return scenario.fake_oauth_token

        mock_fetch_token = create_autospec(
            AsyncOAuth2Client.fetch_token, side_effect=fake_fetch_token
        )
        mp.setattr(
            AsyncOAuth2Client,
            "fetch_token",
            mock_fetch_token,
        )

        # Fake the post() api
        async def fake_post(self, url, params):
            return Response(
                status_code=200,
                json={},
            )

        mock_post = create_autospec(AsyncOAuth2Client.post, side_effect=fake_post)
        mp.setattr(AsyncOAuth2Client, "post", mock_post)

        # Fake the get() api
        async def fake_get(self, url, params):
            return scenario.fake_get_response

        mock_get = create_autospec(AsyncOAuth2Client.get, side_effect=fake_get)
        mp.setattr(AsyncOAuth2Client, "get", mock_get)
        return AuthLibMocks(
            create_authorization_url=mock_create_authorization_url,
            fetch_token=mock_fetch_token,
            post=mock_post,
            get=mock_get,
        )

    return create_fake_oauth_client
