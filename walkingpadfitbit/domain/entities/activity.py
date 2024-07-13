import datetime as dt

from pydantic import BaseModel


class Activity(BaseModel):
    start_time: dt.time
    duration_ms: int
    date: dt.date
    distance_km: float
