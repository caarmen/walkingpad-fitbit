import datetime as dt

from pydantic import BaseModel


class OAuthToken(BaseModel):
    access_token: str
    expires_at: dt.datetime
    refresh_token: str
    user_id: str
