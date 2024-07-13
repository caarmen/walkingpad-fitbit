import uuid
from dataclasses import dataclass
from typing import Any, Callable

import pytest
from authlib.integrations.httpx_client import AsyncOAuth2Client
from httpx import Response


@dataclass
class AuthLibScenario:
    fake_authorization_url: str = "https://fake.fitbit.com/authorize?foo=bar"
    fake_callback_url: str = "https://myapp.com/oauth/fitbit/?abc=def"
    fake_oauth_token: dict[str, Any] | None = None


@pytest.fixture
def fake_oauth_client() -> Callable[[pytest.MonkeyPatch, AuthLibScenario], None]:
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

        mp.setattr(
            AsyncOAuth2Client,
            "create_authorization_url",
            fake_create_authorization_url,
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

        mp.setattr(
            AsyncOAuth2Client,
            "fetch_token",
            fake_fetch_token,
        )

        # Fake the post() api
        async def fake_post(self, url, params):
            return Response(
                status_code=200,
                json={},
            )

        mp.setattr(
            AsyncOAuth2Client,
            "post",
            fake_post,
        )

    return create_fake_oauth_client
