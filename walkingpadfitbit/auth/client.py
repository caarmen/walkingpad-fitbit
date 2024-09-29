import logging
from typing import Any, Protocol

from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.oauth2.auth import OAuth2Token
from httpx import Response

from walkingpadfitbit.auth import storage

logger = logging.getLogger(__name__)


class Client(Protocol):
    async def post(
        url: str,
        params: dict[str, Any],
    ) -> Response: ...


def get_client(
    client_id: str,
    client_secret: str,
) -> Client | None:

    token = storage.read_oauth_token()
    if not token:
        return None

    async def update_token(token: dict[str, Any], **kwargs):
        logger.info("update_token")
        if token.get("success") is False:
            raise Exception("bad refresh token")  # TODO specific exception
        storage.save_oauth_token(OAuth2Token.from_dict(token))

    return AsyncOAuth2Client(
        client_id,
        client_secret,
        token=token,
        token_endpoint="https://api.fitbit.com/oauth2/token",
        update_token=update_token,
    )
