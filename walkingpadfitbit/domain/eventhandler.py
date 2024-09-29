import asyncio
import datetime as dt
import logging
import sys
from io import TextIOBase

from walkingpadfitbit.domain.display.base import BaseDisplay
from walkingpadfitbit.domain.entities.activity import Activity
from walkingpadfitbit.domain.entities.dailysummary import DailySummary
from walkingpadfitbit.domain.entities.event import (
    TreadmillEvent,
    TreadmillStopEvent,
    TreadmillWalkEvent,
)
from walkingpadfitbit.domain.remoterepository import (
    RemoteActivityRepository,
    RepositoryException,
)

logger = logging.getLogger(__name__)


class TreadmillEventHandler:
    def __init__(
        self,
        remote_activity_repository: RemoteActivityRepository,
        display: BaseDisplay,
        event_output: TextIOBase = sys.stdout,
    ):
        self._remote_activity_repository = remote_activity_repository
        self._display = display
        self._last_walk_event: TreadmillWalkEvent = None
        self._event_output = event_output
        self._daily_summary: DailySummary | None = None
        self._schedule_fetch_daily_summary()

    def handle_treadmill_event(self, event: TreadmillEvent):
        logger.debug(f"handle_treadmill_event {event}")
        if event == TreadmillStopEvent:
            self._on_stop()
        else:
            self._on_walk(event)

    async def _fetch_daily_summary(self):
        try:
            self._daily_summary = (
                await self._remote_activity_repository.get_daily_summary()
            )
            logger.info(f"Daily summary is {self._daily_summary}")
        except RepositoryException as e:
            logger.error(f"Couldn't fetch daily summary: {e}")
            self._daily_summary = None

    def _schedule_fetch_daily_summary(self):
        asyncio.create_task(self._fetch_daily_summary())

    def _on_walk(self, event: TreadmillEvent):
        self._print_event_output(event_text=self._display.walk_event_to_text(event))
        self._last_walk_event = event

    def _on_stop(self):
        last_walk_event = self._last_walk_event
        if last_walk_event:
            logger.info("Walk stopped")
            self._print_event_output(event_text=self._display.stop_event_to_text())
            now_utc = dt.datetime.now(tz=dt.timezone.utc)
            now_localtime = now_utc.astimezone()
            activity = Activity(
                start=now_localtime - dt.timedelta(seconds=last_walk_event.time_s),
                duration_ms=last_walk_event.time_s * 1000,
                distance_km=last_walk_event.dist_km,
            )
            asyncio.create_task(
                self._remote_activity_repository.post_activity(activity),
                name="post_activity",
            )
            self._last_walk_event = None

    def _print_event_output(self, event_text: str):
        print(
            event_text,
            file=self._event_output,
            flush=True,
        )

    async def flush(self):
        tasks = [t for t in asyncio.all_tasks() if t.get_name() == "post_activity"]
        await asyncio.gather(*tasks)
