from authlib.integrations.httpx_client import AsyncOAuth2Client

from walkingpadfitbit.auth import storage


def get_client(
    client_id: str,
    client_secret: str,
) -> AsyncOAuth2Client | None:

    token = storage.read_oauth_token()
    if not token:
        return None

    return AsyncOAuth2Client(
        client_id,
        client_secret,
        token=token,
    )
