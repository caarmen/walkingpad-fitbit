from abc import ABC, abstractmethod
from typing import Callable

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
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...
