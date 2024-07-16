import asyncio
import datetime as dt
import logging

from walkingpadfitbit.domain.entities.activity import Activity
from walkingpadfitbit.domain.entities.event import (
    TreadmillEvent,
    TreadmillStopEvent,
    TreadmillWalkEvent,
)
from walkingpadfitbit.domain.remoterepository import RemoteActivityRepository

logger = logging.getLogger(__name__)


class TreadmillEventHandler:
    def __init__(
        self,
        remote_activity_repository: RemoteActivityRepository,
    ):
        self._remote_activity_repository = remote_activity_repository
        self._last_walk_event: TreadmillWalkEvent = None

    def handle_treadmill_event(self, event: TreadmillEvent):
        logger.debug(f"handle_treadmill_event {event}")
        if event == TreadmillStopEvent:
            self._on_stop()
        else:
            self._on_walk(event)

    def _on_walk(self, event: TreadmillEvent):
        self._last_walk_event = event

    def _on_stop(self):
        last_walk_event = self._last_walk_event
        if last_walk_event:
            logger.info("Walk stopped")
            now_utc = dt.datetime.now(tz=dt.timezone.utc)
            now_localtime = now_utc.astimezone()
            activity = Activity(
                start=now_localtime - dt.timedelta(seconds=last_walk_event.time_s),
                duration_ms=last_walk_event.time_s * 1000,
                distance_km=last_walk_event.dist_km,
            )
            asyncio.create_task(
                self._remote_activity_repository.post_activity(activity)
            )
            self._last_walk_event = None
