from walkingpadfitbit.auth.entities.oauth_token import OAuthToken
from walkingpadfitbit.auth.usecases import storage
from walkingpadfitbit.auth.usecases.callback import handle_callback


def test_oauth_callback():
    token: OAuthToken = handle_callback(callback_url="https://anyurl")
    assert token.access_token == "todo"
    saved_token = storage.read_oauth_token()
    assert token == saved_token
