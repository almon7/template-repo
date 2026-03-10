#!/bin/bash
# -e: abort on error  -u: error on unset variables  -o pipefail: propagate pipe failures
set -euo pipefail
# dev-entrypoint.sh
# This script is executed when the dev Docker container starts.
# Runs uvicorn with hot-reload so source changes in the mounted volume take effect immediately.

uv run uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --reload-dir /app/app