import logging
from typing import Any, Coroutine

from bleak.backends.device import BLEDevice
from ph4_walkingpad.pad import Scanner

logger = logging.getLogger(__name__)


class DeviceNotFoundException(Exception): ...


async def get_device(
    device_name: str,
) -> Coroutine[Any, Any, BLEDevice]:
    scanner = Scanner()
    await scanner.scan(dev_name=device_name.lower())

    if not scanner.walking_belt_candidates:
        raise DeviceNotFoundException(f"{device_name} not found")

    device = scanner.walking_belt_candidates[0]
    logger.info(f"Found device {device}")
    return device
