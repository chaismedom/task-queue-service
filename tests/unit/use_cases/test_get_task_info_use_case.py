from datetime import datetime, timedelta

import pytest

from task_queue_service.repositories import AbstractTaskRepository, FakeTaskRepository
from task_queue_service.task import Task, TaskStatus
from task_queue_service.use_cases import GetTaskStatusUseCaseImpl


class TestAddTaskUseCase:
    @pytest.fixture
    def waiting_task(self) -> Task:
        return Task(
            "waiting",
            waiting_time=datetime.now() + timedelta(hours=3),
            status=TaskStatus.WAITING,
        )

    @pytest.fixture
    def expired_task(self) -> Task:
        return Task(
            "done",
            waiting_time=datetime.now() + timedelta(hours=-3),
            status=TaskStatus.DONE,
        )

    @pytest.fixture
    def expired_but_not_polled_task(self) -> Task:
        return Task(
            "done",
            waiting_time=datetime.now() + timedelta(hours=-3),
            status=TaskStatus.WAITING,
        )

    @pytest.fixture
    def task_repository(
        self,
        waiting_task: Task,
        expired_task: Task,
        expired_but_not_polled_task: Task,
    ) -> AbstractTaskRepository:
        return FakeTaskRepository(
            [waiting_task, expired_task, expired_but_not_polled_task]
        )

    @pytest.fixture
    def use_case(
        self,
        task_repository: AbstractTaskRepository,
    ) -> GetTaskStatusUseCaseImpl:
        return GetTaskStatusUseCaseImpl(
            task_repository=task_repository,
        )

    async def test_use_case_waiting_task_success(
        self,
        use_case: GetTaskStatusUseCaseImpl,
        waiting_task: Task,
    ) -> None:
        status = await use_case(waiting_task.id_)
        assert status is TaskStatus.WAITING

    async def test_use_case_done_task_success(
        self,
        use_case: GetTaskStatusUseCaseImpl,
        expired_task: Task,
    ) -> None:
        status = await use_case(expired_task.id_)
        assert status is TaskStatus.DONE

    async def test_use_case_done_task_but_not_polled_success(
        self,
        use_case: GetTaskStatusUseCaseImpl,
        expired_but_not_polled_task: Task,
    ) -> None:
        status = await use_case(expired_but_not_polled_task.id_)
        assert status is TaskStatus.WAITING
