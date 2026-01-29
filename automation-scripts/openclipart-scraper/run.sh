#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$PROJECT_ROOT/src"

python -m openclipart.cli --config conf/config.yml "$@"
