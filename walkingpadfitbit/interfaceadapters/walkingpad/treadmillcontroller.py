import asyncio
import logging
from typing import Annotated, Callable

from annotated_types import Ge, Le
from bleak.backends.device import BLEDevice
from ph4_walkingpad.pad import Controller, WalkingPad, WalkingPadCurStatus

from walkingpadfitbit.domain.entities.event import (
    TreadmillEvent,
    TreadmillStopEvent,
    TreadmillWalkEvent,
)
from walkingpadfitbit.domain.treadmillcontroller import TreadmillController

logger = logging.getLogger(__name__)


class WalkingpadTreadmillController(TreadmillController):
    def __init__(
        self,
        device: BLEDevice,
    ) -> None:
        self.ctler = Controller()
        self.device = device

    def subscribe(self, callback: Callable[[TreadmillEvent], None]) -> None:
        self.ctler.handler_cur_status = lambda _, status: callback(
            _to_treadmill_event(status)
        )

    def is_connected(self) -> bool:
        return self.ctler.client.is_connected

    async def connect(self) -> None:
        await self.ctler.run(self.device)

    async def disconnect(self) -> None:
        await self.ctler.disconnect()

    async def ask_stats(self) -> None:
        await self.ctler.ask_stats()

    def is_on(self) -> bool:
        last_status = self.ctler.last_status
        return last_status and last_status.belt_state == 1

    async def start(self) -> None:
        await self.ctler.switch_mode(WalkingPad.MODE_MANUAL)
        await asyncio.sleep(1)
        logger.info("Starting device...")
        await self.ctler.start_belt()
        logger.info("Started device.")

    async def stop(self) -> None:
        logger.info("Stopping device...")
        await self.ctler.stop_belt()
        logger.info("Stopped device.")
        await asyncio.sleep(3)
        await self.ctler.switch_mode(WalkingPad.MODE_STANDBY)

    async def set_speed(
        self,
        speed_kph: Annotated[float, Ge(0.0)],
    ) -> None:
        await self.ctler.change_speed(int(speed_kph * 10))

    async def change_speed_by(
        self,
        speed_delta_kph: Annotated[float, Le(1.0), Ge(-1.0)],
    ) -> float:
        speed_before_kph: float = (
            self.ctler.last_status.speed / 10 if self.ctler.last_status else 0.0
        )

        new_speed_kph = max(0.0, speed_before_kph + speed_delta_kph)

        await self.ctler.change_speed(int(new_speed_kph * 10))
        return new_speed_kph


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
            speed_kph=status.speed / 10,
        )
    return TreadmillStopEvent
