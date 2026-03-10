#!/bin/bash
# -e: abort on error  -u: error on unset variables  -o pipefail: propagate pipe failures
set -euo pipefail
# prod-entrypoint.sh
# This script is executed when the production Docker container starts.
# Single worker is the recommended default when scaling is handled at the container
# orchestration layer (e.g. Kubernetes, ECS). Increase --workers only if you run many
# containers on a single host and want to utilise multiple CPU cores per container.

echo "Starting production server on 0.0.0.0:8000..."
uv run uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --no-access-log