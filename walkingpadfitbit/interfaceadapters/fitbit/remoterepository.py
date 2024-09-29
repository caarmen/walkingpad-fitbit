import datetime as dt
import logging

from httpx import Response

from walkingpadfitbit.auth.client import Client
from walkingpadfitbit.domain.entities.activity import Activity
from walkingpadfitbit.domain.entities.dailysummary import DailySummary
from walkingpadfitbit.domain.remoterepository import (
    RemoteActivityRepository,
    RepositoryException,
)

logger = logging.getLogger(__name__)

ACTIVITY_TYPE_TREADMILL = 90019


class FitbitRemoteActivityRepository(RemoteActivityRepository):
    def __init__(
        self,
        client: Client,
    ):
        self.client = client

    async def post_activity(self, activity: Activity):
        await self.client.post(
            url="https://api.fitbit.com/1/user/-/activities.json",
            params={
                "date": activity.start.strftime("%Y-%m-%d"),
                "startTime": activity.start.strftime("%H:%M"),
                "durationMillis": activity.duration_ms,
                "distance": activity.distance_km,
                "activityId": ACTIVITY_TYPE_TREADMILL,
                "distanceUnit": "Kilometer",
                "manualCalories": 0,
            },
        )

    async def get_daily_summary(self) -> DailySummary:
        now_utc = dt.datetime.now(tz=dt.timezone.utc)
        now_localtime = now_utc.astimezone()
        response: Response = await self.client.get(
            url="https://api.fitbit.com/1/user/-/activities/list.json",
            params={
                "afterDate": now_localtime.strftime("%Y-%m-%d"),
                "limit": 100,
            },
        )
        if not response.is_success:
            logger.error(f"Error retrieving daily activity summary: {response}")
            raise RepositoryException

        treadmill_activities = [
            activity
            for activity in response.json()["activities"]
            if activity["activityTypeId"] == ACTIVITY_TYPE_TREADMILL
            # TODO handle conversions if needed.
            # All entries logged from this app are in Kilometer. Any conversions would be
            # for Treadmill activities logged outside this app.
            and activity["distanceUnit"] == "Kilometer"
        ]

        return DailySummary(
            total_duration_ms=sum(
                activity["duration"] for activity in treadmill_activities
            ),
            total_distance_km=sum(
                activity["distance"] for activity in treadmill_activities
            ),
        )
