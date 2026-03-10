#!/bin/bash
# -e: abort on error  -u: error on unset variables  -o pipefail: propagate pipe failures
set -euo pipefail
# run-tests.sh
# This script runs the test suite for the codebase and checks coverage.
#
# Usage:
#   bash scripts/run-tests.sh [TEST_DIR] [APP_DIR]
#
# Arguments:
#   TEST_DIR   Directory containing test files (default: /app/tests)
#   APP_DIR    Directory containing application code for coverage (default: /app/app)
#
# Example:
#   bash scripts/run-tests.sh tests src/app

# Use argument if provided, otherwise default to Docker path
TEST_DIR="${1:-/app/tests}"
APP_DIR="${2:-/app/app}"

echo "Running tests..."
uv run pytest --cov="${APP_DIR}" "${TEST_DIR}"
