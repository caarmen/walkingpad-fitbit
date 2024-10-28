import asyncio
import logging

from ph4_walkingpad.pad import Controller, WalkingPad

from walkingpadfitbit.interfaceadapters.walkingpad.device import get_device

logger = logging.getLogger(__name__)


async def stop_device(device_name: str):
    # 1. Find the device with the given name.
    device = await get_device(device_name)

    # 2. Run the controller for the found device.
    ctler = Controller()
    await ctler.run(device)

    logger.info("Stopping device...")
    await ctler.stop_belt()
    logger.info("Stopped device.")
    await asyncio.sleep(3)

    await ctler.switch_mode(WalkingPad.MODE_STANDBY)
