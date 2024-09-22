from abc import ABC, abstractmethod

from walkingpadfitbit.domain.entities.event import TreadmillWalkEvent


class BaseDisplay(ABC):
    @abstractmethod
    def walk_event_to_text(
        self,
        event: TreadmillWalkEvent,
    ) -> str:
        raise NotImplementedError
