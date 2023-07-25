from datetime import datetime, timedelta

import pytest

from task_queue_service.repositories import AbstractTaskRepository, FakeTaskRepository
from task_queue_service.services.task_queue import TaskQueueService
from task_queue_service.task import Task


class TestTaskQueueService:
    @pytest.fixture
    def tasks(self) -> list[Task]:
        return [
            Task("waiting1", waiting_time=datetime.now() + timedelta(hours=1)),
            Task("waiting2", waiting_time=datetime.now() + timedelta(hours=2)),
            Task("expired1", waiting_time=datetime.now() + timedelta(seconds=-10)),
            Task("expired2", waiting_time=datetime.now() + timedelta(seconds=-30)),
        ]

    @pytest.fixture
    def task_repository(self, tasks: list[Task]) -> AbstractTaskRepository:
        return FakeTaskRepository(tasks)

    @pytest.fixture
    def task_queue(self, task_repository: AbstractTaskRepository) -> TaskQueueService:
        return TaskQueueService(
            task_repository=task_repository,
        )

    async def test_queue_poll_success(
        self, task_queue: TaskQueueService, task_repository: AbstractTaskRepository
    ) -> None:
        await task_queue.poll()
        expired_tasks = await task_repository.list_expired()
        assert {task.title for task in expired_tasks} == {"expired1", "expired2"}
