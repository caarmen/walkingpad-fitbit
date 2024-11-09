from typing import Callable

from bleak.backends.device import BLEDevice
from ph4_walkingpad.pad import Controller, WalkingPadCurStatus

from walkingpadfitbit.domain.entities.event import (
    TreadmillEvent,
    TreadmillStopEvent,
    TreadmillWalkEvent,
)
from walkingpadfitbit.domain.treadmillcontroller import TreadmillController


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
