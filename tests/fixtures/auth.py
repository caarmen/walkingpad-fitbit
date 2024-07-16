import pytest
from authlib.oauth2.auth import OAuth2Token

from walkingpadfitbit.auth import storage
from walkingpadfitbit.auth.client import Client, get_client
from walkingpadfitbit.auth.config import Settings


@pytest.fixture
def client() -> Client:
    storage.save_oauth_token(OAuth2Token({"access_token": "some access token"}))
    settings = Settings(_env_file=".env.test")
    oauth_settings = {
        "client_id": settings.fitbit_oauth_client_id,
        "client_secret": settings.fitbit_oauth_client_secret,
    }
    return get_client(**oauth_settings)
