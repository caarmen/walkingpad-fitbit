import logging
from typing import Any, Coroutine, Protocol

from bleak.backends.device import BLEDevice

logger = logging.getLogger(__name__)


class DeviceNotFoundException(Exception): ...


class ScannerProtocol(Protocol):
    async def scan(self, *args, **kwargs): ...

    @property
    def walking_belt_candidates(self) -> list[BLEDevice]: ...


async def get_device(
    device_name: str,
    scanner: ScannerProtocol,
) -> Coroutine[Any, Any, BLEDevice]:
    await scanner.scan(dev_name=device_name.lower())

    if not scanner.walking_belt_candidates:
        raise DeviceNotFoundException(f"{device_name} not found")

    device = scanner.walking_belt_candidates[0]
    logger.info(f"Found device {device}")
    return device
