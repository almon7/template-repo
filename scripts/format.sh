#!/bin/bash
# -e: abort on error  -u: error on unset variables  -o pipefail: propagate pipe failures
set -euo pipefail
# format.sh
# This script runs code formatting tools on the codebase.

APP_DIR="${1:-/app/app}"
TEST_DIR="${2:-/app/tests}"

echo "Running ruff format on ${APP_DIR} and ${TEST_DIR}..."
uv run ruff format "${APP_DIR}" "${TEST_DIR}"
echo "ruff format complete."

echo "Running ruff lint --fix on ${APP_DIR} and ${TEST_DIR}..."
uv run ruff check --fix "${APP_DIR}" "${TEST_DIR}"
echo "ruff lint complete."

echo "All formatting checks done."