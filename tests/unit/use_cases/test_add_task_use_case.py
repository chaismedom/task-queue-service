from datetime import datetime, timedelta

import pytest

from task_queue_service.repositories import FakeTaskRepository
from task_queue_service.services.task_timer import (
    AbstractTaskTimerService,
    FakeTaskTimerService,
)
from task_queue_service.uow import AbstractUnitOfWork, FakeUnitOfWork
from task_queue_service.use_cases import AddTaskUseCaseImpl


class TestAddTaskUseCase:
    @pytest.fixture
    def waiting_time(self) -> datetime:
        return datetime.now() + timedelta(seconds=40)

    @pytest.fixture
    def task_timer(self, waiting_time: datetime) -> AbstractTaskTimerService:
        return FakeTaskTimerService(waiting_time)

    @pytest.fixture
    def task_repository(self) -> FakeTaskRepository:
        return FakeTaskRepository()

    @pytest.fixture
    def uow(self, task_repository: FakeTaskRepository) -> AbstractUnitOfWork:
        return FakeUnitOfWork(task_repository=task_repository)

    @pytest.fixture
    def use_case(
        self,
        uow: AbstractUnitOfWork,
        task_timer: AbstractTaskTimerService,
    ) -> AddTaskUseCaseImpl:
        return AddTaskUseCaseImpl(
            uow=uow,
            task_timer=task_timer,
        )

    async def test_use_case_success(
        self,
        waiting_time: datetime,
        use_case: AddTaskUseCaseImpl,
        uow: AbstractUnitOfWork,
    ) -> None:
        title = "test-title"

        task_id = await use_case(title)
        async with uow:
            task = await uow.task_repository.get_by_id(task_id)
        assert task.title == title
        assert task.waiting_time == waiting_time
