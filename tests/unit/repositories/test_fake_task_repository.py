from datetime import datetime
from uuid import uuid4

import pytest

from task_queue_service.repositories import FakeTaskRepository, TaskNotFoundError
from task_queue_service.task import Task


class TestFakeTaskRepository:
    @pytest.fixture
    def task_repository(self) -> FakeTaskRepository:
        return FakeTaskRepository()

    async def test_get_by_id_success(self) -> None:
        task = Task(title="foo", waiting_time=datetime.now())
        repository = FakeTaskRepository(db=[task])

        task_from_db = await repository.get_by_id(task.id_)
        assert task == task_from_db

    async def test_get_by_id_fail(self) -> None:
        task = Task(title="bar", waiting_time=datetime.now())
        repository = FakeTaskRepository(db=[task])

        non_existent_id = uuid4()
        with pytest.raises(TaskNotFoundError):
            await repository.get_by_id(non_existent_id)
