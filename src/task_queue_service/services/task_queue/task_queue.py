from task_queue_service.repositories import AbstractTaskRepository
from task_queue_service.services.task_queue.interface import AbstractTaskQueueService


class TaskQueueService(AbstractTaskQueueService):
    def __init__(self, task_repository: AbstractTaskRepository) -> None:
        self._task_repository = task_repository

    async def poll(self) -> None:
        tasks = await self._task_repository.list_expired()
        for task in tasks:
            task.mark_done()
            await self._task_repository.persist(task)

        await self._task_repository.commit()
