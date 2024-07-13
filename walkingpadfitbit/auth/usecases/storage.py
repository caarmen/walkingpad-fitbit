import keyring

from walkingpadfitbit.auth.entities.oauth_token import OAuthToken

SERVICE_NAME = "walkingpad-fitbit"
DEFAULT_USER = "defaultuser"


def save_oauth_token(
    token: OAuthToken,
    username: str = DEFAULT_USER,
):
    keyring.set_password(
        service_name=SERVICE_NAME,
        username=username,
        password=token.model_dump_json(),
    )


def read_oauth_token(
    username: str = DEFAULT_USER,
):
    token_str = keyring.get_password(
        service_name=SERVICE_NAME,
        username=username,
    )
    return OAuthToken.model_validate_json(token_str)
