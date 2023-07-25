from task_queue_service.services.task_queue import AbstractTaskQueueService
from task_queue_service.use_cases.interface import AbstractPollTasksUseCase


class PollTasksUseCaseImpl(AbstractPollTasksUseCase):
    def __init__(
        self,
        task_queue: AbstractTaskQueueService,
    ) -> None:
        self._task_queue = task_queue

    async def __call__(self) -> None:
        await self._task_queue.poll()
