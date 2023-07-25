import random
from datetime import datetime, timedelta

from task_queue_service.services.task_timer.interface import AbstractTaskTimerService


class RandomTaskTimerService(AbstractTaskTimerService):
    def __init__(self, low_time_limit: timedelta, high_time_limit: timedelta) -> None:
        assert low_time_limit <= high_time_limit
        self._low_time_limit = int(low_time_limit.total_seconds())
        self._high_time_limit = int(high_time_limit.total_seconds())

    def __call__(self) -> datetime:
        random_seconds = random.randint(
            self._low_time_limit,
            self._high_time_limit,
        )
        return datetime.now() + timedelta(seconds=random_seconds)
