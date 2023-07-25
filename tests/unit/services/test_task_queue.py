from datetime import datetime, timedelta

import pytest

from task_queue_service.repositories import FakeTaskRepository
from task_queue_service.services.task_queue import TaskQueueService
from task_queue_service.task import Task
from task_queue_service.uow import AbstractUnitOfWork, FakeUnitOfWork


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
    def task_repository(self, tasks: list[Task]) -> FakeTaskRepository:
        return FakeTaskRepository(tasks)

    @pytest.fixture
    def uow(self, task_repository: FakeTaskRepository) -> AbstractUnitOfWork:
        return FakeUnitOfWork(task_repository=task_repository)

    @pytest.fixture
    def task_queue(self, uow: AbstractUnitOfWork) -> TaskQueueService:
        return TaskQueueService(uow=uow)

    async def test_queue_poll_success(
        self,
        task_queue: TaskQueueService,
        uow: AbstractUnitOfWork,
    ) -> None:
        await task_queue.poll()
        async with uow:
            expired_tasks = await uow.task_repository.list_expired()

        assert {task.title for task in expired_tasks} == {"expired1", "expired2"}
