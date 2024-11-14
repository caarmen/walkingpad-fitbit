from abc import ABC, abstractmethod
from typing import Annotated, Callable

from annotated_types import Ge, Le

from walkingpadfitbit.domain.entities.event import TreadmillEvent


class TreadmillController(ABC):
    @abstractmethod
    def subscribe(self, callback: Callable[[TreadmillEvent], None]) -> None: ...

    @abstractmethod
    def is_connected(self) -> bool: ...

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    async def ask_stats(self) -> None: ...

    @abstractmethod
    def is_on(self) -> bool: ...

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...

    @abstractmethod
    async def change_speed_by(
        self,
        speed_delta_kph: Annotated[float, Le(1.0), Ge(-1.0)],
    ) -> float:
        """
        Increase or decrease the current treadmill speed by the given delta.
        :param speed_delta_kph: the difference (negative or positive) speed in km/h to apply to the current speed.

        :return: the new treadmill speed.
        """
