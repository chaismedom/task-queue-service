from uuid import UUID

from task_queue_service.repositories.interface import AbstractTaskRepository
from task_queue_service.services.task_timer import AbstractTaskTimerService
from task_queue_service.task import Task
from task_queue_service.use_cases.interface import AbstractAddTaskUseCase


class AddTaskUseCaseImpl(AbstractAddTaskUseCase):
    def __init__(
        self,
        task_timer: AbstractTaskTimerService,
        task_repository: AbstractTaskRepository,
    ) -> None:
        self._task_timer = task_timer
        self._task_repository = task_repository

    async def __call__(self, task_title: str) -> UUID:
        task = Task(
            title=task_title,
            waiting_time=self._task_timer(),
        )
        await self._task_repository.add(task)
        await self._task_repository.commit()
        return task.id_
