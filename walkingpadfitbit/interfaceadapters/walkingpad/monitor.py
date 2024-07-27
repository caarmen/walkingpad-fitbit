import asyncio
import logging
import signal
import time
from asyncio import sleep

from ph4_walkingpad.pad import Controller, Scanner, WalkingPadCurStatus

from walkingpadfitbit.domain.entities.event import (
    TreadmillEvent,
    TreadmillStopEvent,
    TreadmillWalkEvent,
)
from walkingpadfitbit.domain.eventhandler import TreadmillEventHandler

logger = logging.getLogger(__name__)


program_end_event = asyncio.Event()


def on_cur_status_received(
    status: WalkingPadCurStatus,
    treadmill_event_handler: TreadmillEventHandler,
):
    treadmill_event = _to_treadmill_event(status)
    if treadmill_event:
        treadmill_event_handler.handle_treadmill_event(treadmill_event)


def _to_treadmill_event(status: WalkingPadCurStatus) -> TreadmillEvent:
    # status.dist is "distance in 10 meters"
    # distance_m = status.dist * 10
    # distance_km = distance_m / 1000
    #   = (status.dist * 10) / 1000
    #   = status.dist / 100

    # https://github.com/ph4r05/ph4-walkingpad/tree/master?tab=readme-ov-file#protocol-basics
    if status.belt_state == 1:
        return TreadmillWalkEvent(
            time_s=status.time,
            dist_km=status.dist / 100,
        )
    return TreadmillStopEvent


async def monitor(
    device_name: str,
    treadmill_event_handler: TreadmillEventHandler,
    monitor_duration_s: float | None = None,
    poll_interval_s: float = 1.0,
):
    """
    1. Find the device with the given name.
    2. Run the controller for the found device.
    3. Loop, asking the controller for stats.
    """

    # 1. Find the device with the given name.
    scanner = Scanner()
    await scanner.scan(dev_name=device_name.lower())

    if not scanner.walking_belt_candidates:
        logger.error(f"{device_name} not found")
        return

    device = scanner.walking_belt_candidates[0]
    logger.info(f"Found device {device}")

    # 2. Run the controller for the found device.
    ctler = Controller()
    ctler.handler_cur_status = lambda _, status: on_cur_status_received(
        status, treadmill_event_handler
    )

    await ctler.run(device)
    # 3. Loop, asking the controller for stats.
    start_timestamp = time.time()
    stop_timestamp = (
        start_timestamp + monitor_duration_s if monitor_duration_s else None
    )

    program_end_event.clear()
    while not program_end_event.is_set():
        await ctler.ask_stats()
        if stop_timestamp and time.time() > stop_timestamp:
            # Send an event signaling the end of the walk, so it can be logged
            # if it wasn't logged already:
            treadmill_event_handler.handle_treadmill_event(TreadmillStopEvent)
            await treadmill_event_handler.flush()
            break
        await sleep(poll_interval_s)

        if not ctler.client.is_connected:
            logger.info("Got disconnected. Reconnecting...")
            await ctler.disconnect()
            await sleep(5)
            try:
                await ctler.run(device)
            except TimeoutError:
                logger.warning("Timeout trying to reconnect")

    logger.info("Stop monitoring")


def signal_handler(signum, frame):
    program_end_event.set()


signal.signal(signal.SIGINT, signal_handler)
