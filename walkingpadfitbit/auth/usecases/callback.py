import datetime as dt

from walkingpadfitbit.auth.entities.oauth_token import OAuthToken
from walkingpadfitbit.auth.usecases import storage


def handle_callback(
    callback_url: str,
) -> OAuthToken:
    token = parse_oauth_token(callback_url)
    storage.save_oauth_token(token)
    return token


def parse_oauth_token(
    callback_url: str,
) -> OAuthToken:
    return OAuthToken(
        access_token="todo",
        expires_at=dt.datetime(2030, 1, 1, 1, 1, 1, tzinfo=dt.timezone.utc),
        refresh_token="todo",
        user_id="1234",
    )
