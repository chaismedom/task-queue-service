from datetime import timedelta

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    poll_timeout: timedelta = timedelta(seconds=5)
    add_time_low_limit: timedelta = timedelta(seconds=5)
    add_time_high_limit: timedelta = timedelta(seconds=10)

    postgres_host: str = Field(validation_alias="POSTGRES_HOST")
    postgres_port: str = Field(validation_alias="POSTGRES_PORT")
    postgres_db: str = Field(validation_alias="POSTGRES_DB")
    postgres_user: str = Field(validation_alias="POSTGRES_USER")
    postgres_password: str = Field(validation_alias="POSTGRES_PASSWORD")
