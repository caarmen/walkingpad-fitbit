import datetime as dt

from pydantic import BaseModel


class Activity(BaseModel):
    start: dt.datetime
    duration_ms: int
    distance_km: float
