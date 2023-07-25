from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from task_queue_service.task import TaskStatus
from task_queue_service.use_cases import (
    AbstractAddTaskUseCase,
    AbstractGetTaskStatusUseCase,
)

router = APIRouter(tags=["tasks"])


class CreateTaskInput(BaseModel):
    title: str


class CreateTaskOutput(BaseModel):
    task_id: UUID


class GetTaskStatusOutput(BaseModel):
    task_status: TaskStatus


@router.post("/tasks/")
@inject
async def create_task(
    task_input: CreateTaskInput,
    use_case: AbstractAddTaskUseCase = Depends(Provide["add_task_use_case"]),
) -> CreateTaskOutput:
    task_id = await use_case(
        task_title=task_input.title,
    )
    return CreateTaskOutput(task_id=task_id)


@router.get("/tasks/{task_id}/status/")
@inject
async def get_task_status(
    task_id: UUID,
    use_case: AbstractGetTaskStatusUseCase = Depends(
        Provide["get_task_status_use_case"],
    ),
) -> GetTaskStatusOutput:
    task_status = await use_case(task_id=task_id)
    return GetTaskStatusOutput(task_status=task_status)
