from datetime import timedelta

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    poll_timeout: timedelta = timedelta(seconds=5)
    add_time_low_limit: timedelta = timedelta(seconds=5)
    add_time_high_limit: timedelta = timedelta(seconds=10)
