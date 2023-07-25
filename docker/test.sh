#!/bin/bash

set -euf -o pipefail

export COVERAGE_FILE=/tmp/.coverage

exec pytest -p no:cacheprovider $@
