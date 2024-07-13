import webbrowser

from walkingpadfitbit.auth.login import login


async def login_cli(
    client_id: str,
    client_secret: str,
) -> None:

    login_flow = login(
        client_id=client_id,
        client_secret=client_secret,
    )
    auth_uri = await anext(login_flow)
    print(f"Open {auth_uri}")
    webbrowser.open(auth_uri)
    callback_url = input("Paste the callback url here:")
    await login_flow.asend(callback_url)
