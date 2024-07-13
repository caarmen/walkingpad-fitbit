import asyncio

from walkingpadfitbit.auth.usecases.config import Settings
from walkingpadfitbit.interfaceadapters.cli.logincli import login_cli


async def main(
    env_file: str = ".env",
):
    settings = Settings(_env_file=env_file)
    await login_cli(
        client_id=settings.fitbit_oauth_client_id,
        client_secret=settings.fitbit_oauth_client_secret,
    )


if __name__ == "__main__":
    asyncio.run(main())
