from abc import ABC, abstractmethod

from walkingpadfitbit.domain.entities.activity import Activity


class RemoteActivityRepository(ABC):
    @abstractmethod
    async def post_activity(activity: Activity): ...
