#!/bin/bash

isort src/task_queue_service tests
black src/task_queue_service tests
mypy src/task_queue_service tests
flake8 src/task_queue_service tests
