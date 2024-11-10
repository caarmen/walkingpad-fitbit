import asyncio
import logging
import sys

from walkingpadfitbit import container
from walkingpadfitbit.auth.client import get_client
from walkingpadfitbit.auth.config import Settings
from walkingpadfitbit.domain.display.factory import get_display
from walkingpadfitbit.domain.monitoring.eventhandler import TreadmillEventHandler
from walkingpadfitbit.domain.monitoring.monitor import monitor
from walkingpadfitbit.interfaceadapters.cli.argparser import CliArgs, parse_args
from walkingpadfitbit.interfaceadapters.cli.logincli import login_cli
from walkingpadfitbit.interfaceadapters.fitbit.remoterepository import (
    FitbitRemoteActivityRepository,
)
from walkingpadfitbit.interfaceadapters.restapi.server import run_server
from walkingpadfitbit.interfaceadapters.walkingpad.device import DeviceNotFoundException


async def main(
    env_file: str = ".env",
):
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stderr,
        format="[%(asctime)s][%(levelname)-7s][%(name)-10s] %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Get command-line arguments.
    args: CliArgs = parse_args()
    container.config.set("device.name", args.device_name)

    # Log into Fitbit
    settings = Settings(_env_file=env_file)
    oauth_settings = {
        "client_id": settings.fitbit_oauth_client_id,
        "client_secret": settings.fitbit_oauth_client_secret,
    }
    client = get_client(**oauth_settings)
    if not client:
        await login_cli(**oauth_settings)
        client = get_client(**oauth_settings)

    try:
        async with asyncio.TaskGroup() as tg:
            # Start monitoring
            tg.create_task(
                monitor(
                    treadmill_event_handler=TreadmillEventHandler(
                        remote_activity_repository=FitbitRemoteActivityRepository(
                            client
                        ),
                        display=get_display(args.display_mode),
                    ),
                    monitor_duration_s=args.monitor_duration_s,
                    poll_interval_s=args.poll_interval_s,
                )
            )

            # Start the REST api server
            tg.create_task(
                run_server(
                    host=args.server_host,
                    port=args.server_port,
                )
            )
    except* DeviceNotFoundException as e_group:
        logger.error(e_group.exceptions[0])


if __name__ == "__main__":
    asyncio.run(main())
