from datetime import datetime, timedelta

import pytest

from task_queue_service.repositories import AbstractTaskRepository, FakeTaskRepository
from task_queue_service.services.task_timer import (
    AbstractTaskTimerService,
    FakeTaskTimerService,
)
from task_queue_service.use_cases import AddTaskUseCaseImpl


class TestAddTaskUseCase:
    @pytest.fixture
    def waiting_time(self) -> datetime:
        return datetime.now() + timedelta(seconds=40)

    @pytest.fixture
    def task_timer(self, waiting_time: datetime) -> AbstractTaskTimerService:
        return FakeTaskTimerService(waiting_time)

    @pytest.fixture
    def task_repository(self) -> AbstractTaskRepository:
        return FakeTaskRepository()

    @pytest.fixture
    def use_case(
        self,
        task_repository: AbstractTaskRepository,
        task_timer: AbstractTaskTimerService,
    ) -> AddTaskUseCaseImpl:
        return AddTaskUseCaseImpl(
            task_repository=task_repository,
            task_timer=task_timer,
        )

    async def test_use_case_success(
        self,
        waiting_time: datetime,
        use_case: AddTaskUseCaseImpl,
        task_repository: AbstractTaskRepository,
    ) -> None:
        title = "test-title"

        task_id = await use_case(title)

        task = await task_repository.get_by_id(task_id)
        assert task.title == title
        assert task.waiting_time == waiting_time
