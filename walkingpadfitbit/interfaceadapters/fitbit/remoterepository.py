from walkingpadfitbit.auth.client import Client
from walkingpadfitbit.domain.entities.activity import Activity
from walkingpadfitbit.domain.remoterepository import RemoteActivityRepository


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
                "startTime": activity.start_time.strftime("%H:%M"),
                "durationMillis": activity.duration_ms,
                "date": activity.date.strftime("%Y-%m-%d"),
                "distance": activity.distance_km,
                "activityId": 90019,
                "distanceUnit": "Kilometer",
            },
        )
