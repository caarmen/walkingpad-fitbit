import logging

from authlib.integrations.httpx_client import AsyncOAuth2Client

from walkingpadfitbit.domain.entities.activity import Activity
from walkingpadfitbit.domain.remoterepository import RemoteActivityRepository

logger = logging.getLogger(__name__)


class FitbitRemoteActivityRepository(RemoteActivityRepository):
    def __init__(
        self,
        client: AsyncOAuth2Client,
    ):
        self.client = client

    async def post_activity(self, activity: Activity):
        response = await self.client.post(
            url="https://api.fitbit.com/1/user/-/activities.json",
            params={
                "startTime": activity.start_time.strftime("%H:%M"),
                "durationMillis": activity.duration_ms,
                "date": activity.date.strftime("%Y-%m-%d"),
                "distance": activity.distance_km,
                "activityId": 90019,
                "distanceUnit": "Kilometer",
            },
        )
        print(f"Posted activity: response={response}")
