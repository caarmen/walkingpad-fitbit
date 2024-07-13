from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    fitbit_oauth_client_id: str
    fitbit_oauth_client_secret: str

    model_config = SettingsConfigDict(
        env_file=".env",
    )
