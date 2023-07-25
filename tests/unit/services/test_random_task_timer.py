from datetime import datetime, timedelta

import pytest

from task_queue_service.services.task_timer import RandomTaskTimerService


class TestTaskQueueService:
    async def test_task_timer_wrong_arguments_fail(self) -> None:
        low_limit = timedelta(seconds=10)
        high_limit = timedelta(seconds=5)
        with pytest.raises(AssertionError):
            RandomTaskTimerService(
                low_time_limit=low_limit,
                high_time_limit=high_limit,
            )

    async def test_task_timer_success(self) -> None:
        low_limit = timedelta(seconds=1)
        high_limit = timedelta(seconds=10)
        service = RandomTaskTimerService(
            low_time_limit=low_limit,
            high_time_limit=high_limit,
        )
        random_time = service()
        approximate_low_limit_time = datetime.now() + timedelta(seconds=-10)
        approximate_high_limit_time = datetime.now() + timedelta(seconds=20)

        assert approximate_low_limit_time <= random_time <= approximate_high_limit_time
