import json

import keyring
from authlib.oauth2.auth import OAuth2Token

SERVICE_NAME = "walkingpad-fitbit"
DEFAULT_USER = "defaultuser"


def save_oauth_token(
    token: OAuth2Token,
    username: str = DEFAULT_USER,
):
    keyring.set_password(
        service_name=SERVICE_NAME,
        username=username,
        password=json.dumps(token),
    )


def read_oauth_token(
    username: str = DEFAULT_USER,
) -> OAuth2Token | None:
    token_str = keyring.get_password(
        service_name=SERVICE_NAME,
        username=username,
    )
    return OAuth2Token.from_dict(json.loads(token_str)) if token_str else None
