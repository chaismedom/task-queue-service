from datetime import datetime

from task_queue_service.services.task_timer.interface import AbstractTaskTimerService


class FakeTaskTimerService(AbstractTaskTimerService):
    def __init__(self, set_time: datetime) -> None:
        self.set_time = set_time

    def __call__(self) -> datetime:
        return self.set_time
