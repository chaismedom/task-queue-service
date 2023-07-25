from datetime import datetime

from task_queue_service.services.task_timer import FakeTaskTimerService


class TestTaskQueueService:
    async def test_task_timer_success(self) -> None:
        time = datetime.now()
        service = FakeTaskTimerService(
            set_time=time,
        )
        result_time = service()
        assert time == result_time
