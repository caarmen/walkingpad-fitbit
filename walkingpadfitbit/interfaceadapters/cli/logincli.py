import webbrowser

from walkingpadfitbit.auth.entities.oauth_token import OAuthToken
from walkingpadfitbit.auth.usecases.login import login


async def login_cli(
    client_id: str,
    client_secret: str,
) -> OAuthToken:

    login_flow = login(
        client_id=client_id,
        client_secret=client_secret,
    )
    auth_uri = await anext(login_flow)
    print(f"Open {auth_uri}")
    webbrowser.open(auth_uri)
    callback_url = input("Paste the callback url here:")
    token: OAuthToken = await login_flow.asend(callback_url)
    return token
