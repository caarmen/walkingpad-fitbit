from typing import AsyncGenerator

from authlib.common.security import generate_token
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.oauth2 import OAuth2Error
from authlib.oauth2.auth import OAuth2Token

from walkingpadfitbit.auth import storage


class AuthError(Exception):
    pass


async def login(
    client_id: str,
    client_secret: str,
) -> AsyncGenerator[str, str]:
    """

    There are two interactions with this async generator:

    1. It yields the authorization url which the user will have to open in
    their browser.

    When the user approves the access in the browser, the browser
    will attempt to redirect to a callback url to complete the login.

    2. The generator expects to be "sent" this callback url.

    """
    base_url = "https://www.fitbit.com/oauth2"
    client = AsyncOAuth2Client(
        client_id,
        client_secret,
        scope="activity",
        code_challenge_method="S256",
    )
    code_verifier = generate_token(48)
    authorization_uri, state = client.create_authorization_url(
        f"{base_url}/authorize",
        code_verifier=code_verifier,
        response_type="code",
    )

    # 1. Yield the authorization url which the user will have to open in
    # their browser.

    # 2. In exchange, expect to be sent the callback url.
    callback_url: str = yield authorization_uri

    callback_url = callback_url.replace("#_=_", "")

    client.state = state

    try:
        response_dict: dict = await client.fetch_token(
            "https://api.fitbit.com/oauth2/token",
            authorization_response=callback_url,
            code_verifier=code_verifier,
        )
        if response_dict.get("success") is False:
            raise AuthError(f"{response_dict}")
    except OAuth2Error as e:
        raise AuthError(f"{e.get_error_description()}") from e

    token_obj = OAuth2Token.from_dict(response_dict)
    storage.save_oauth_token(token_obj)
    yield
