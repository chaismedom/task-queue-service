#!/bin/bash

set -euf -o pipefail

exec poetry run python src/task_queue_service/worker_run.py
