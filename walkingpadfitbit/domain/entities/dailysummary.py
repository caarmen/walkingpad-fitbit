from pydantic import BaseModel


class DailySummary(BaseModel):
    total_duration_ms: int = 0
    total_distance_km: float = 0.0
