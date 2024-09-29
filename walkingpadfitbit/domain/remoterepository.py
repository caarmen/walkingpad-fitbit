from abc import ABC, abstractmethod

from walkingpadfitbit.domain.entities.activity import Activity
from walkingpadfitbit.domain.entities.dailysummary import DailySummary


class RepositoryException(Exception): ...


class RemoteActivityRepository(ABC):
    @abstractmethod
    async def post_activity(self, activity: Activity): ...

    @abstractmethod
    async def get_daily_summary(self) -> DailySummary: ...
