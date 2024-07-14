import asyncio
import datetime as dt
import logging

from walkingpadfitbit.auth.client import get_client
from walkingpadfitbit.auth.config import Settings
from walkingpadfitbit.domain.entities.activity import Activity
from walkingpadfitbit.interfaceadapters.cli.logincli import login_cli
from walkingpadfitbit.interfaceadapters.fitbit.remoterepository import (
    FitbitRemoteActivityRepository,
)


async def main(
    env_file: str = ".env",
):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s][%(levelname)-7s][%(name)-10s] %(message)s",
    )
    settings = Settings(_env_file=env_file)
    oauth_settings = {
        "client_id": settings.fitbit_oauth_client_id,
        "client_secret": settings.fitbit_oauth_client_secret,
    }
    client = get_client(**oauth_settings)
    if not client:
        await login_cli(**oauth_settings)
        client = get_client(**oauth_settings)

    activity_poster = FitbitRemoteActivityRepository(client)
    # Send fake activity for now
    await activity_poster.post_activity(
        activity=Activity(
            start=dt.datetime.now(tz=dt.timezone.utc).replace(
                hour=10, minute=30, second=0, microsecond=0
            ),
            duration_ms=1200000,
            distance_km=1.6,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
