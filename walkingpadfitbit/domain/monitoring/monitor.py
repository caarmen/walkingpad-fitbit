import asyncio
import logging
import signal
import time
from asyncio import sleep
from typing import Any, Awaitable, Callable

from walkingpadfitbit.domain.entities.event import TreadmillStopEvent
from walkingpadfitbit.domain.monitoring.eventhandler import TreadmillEventHandler
from walkingpadfitbit.domain.treadmillcontroller import TreadmillController

logger = logging.getLogger(__name__)


program_end_event = asyncio.Event()


async def _safe_call(
    fn: Callable[..., Awaitable[Any]],
    *args,
    **kwargs,
) -> None:
    try:
        await fn(*args, **kwargs)
    except Exception as e:
        logger.exception("Exception: %s", e)


async def monitor(
    ctler: TreadmillController,
    treadmill_event_handler: TreadmillEventHandler,
    monitor_duration_s: float | None = None,
    poll_interval_s: float = 1.0,
):
    """
    1. Find the device with the given name.
    2. Run the controller for the found device.
    3. Loop, asking the controller for stats.
    """
    ctler.subscribe(treadmill_event_handler.handle_treadmill_event)

    await ctler.connect()
    # 3. Loop, asking the controller for stats.
    start_timestamp = time.time()
    stop_timestamp = (
        start_timestamp + monitor_duration_s if monitor_duration_s else None
    )

    program_end_event.clear()
    while not program_end_event.is_set():
        await _safe_call(ctler.ask_stats)
        if stop_timestamp and time.time() > stop_timestamp:
            # Send an event signaling the end of the walk, so it can be logged
            # if it wasn't logged already:
            treadmill_event_handler.handle_treadmill_event(TreadmillStopEvent)
            await treadmill_event_handler.flush()
            break
        await sleep(poll_interval_s)

        # In case the user ctrl-C'd during the sleep, let's
        # exit early, without checking if we need to reconnect.
        if program_end_event.is_set():
            break

        if not ctler.is_connected():
            logger.info("Got disconnected. Reconnecting...")
            await _safe_call(ctler.disconnect)
            await sleep(5)
            await _safe_call(ctler.connect)

    logger.info("Stop monitoring")


def signal_handler(signum, frame):
    logger.info(f"Signal {signum} received")
    program_end_event.set()


signal.signal(signal.SIGINT, signal_handler)
