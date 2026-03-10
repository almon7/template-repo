#!/bin/bash
# -e: abort on error  -u: error on unset variables  -o pipefail: propagate pipe failures
set -euo pipefail
# format.sh
# This script runs code formatting tools on the codebase.

APP_DIR="${1:-/app/app}"

echo "Running ruff format..."
uv run ruff format "${APP_DIR}"

echo "Running ruff lint --fix..."
uv run ruff check --fix "${APP_DIR}"