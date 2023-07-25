#!/bin/bash

set -euf -o pipefail

exec python src/task_queue_service/worker_run.py
