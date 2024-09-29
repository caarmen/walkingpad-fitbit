from abc import ABC, abstractmethod

from walkingpadfitbit.domain.entities.dailysummary import DailySummary
from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


class BaseDisplay(ABC):
    @abstractmethod
    def walk_event_to_text(
        self,
        event: TreadmillWalkEvent,
        daily_summary: DailySummary | None,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def stop_event_to_text(
        self,
        last_event: TreadmillWalkEvent,
        daily_summary: DailySummary | None,
    ) -> str:
        raise NotImplementedError
