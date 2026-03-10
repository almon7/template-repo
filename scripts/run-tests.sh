#!/bin/bash
# -e: abort on error  -u: error on unset variables  -o pipefail: propagate pipe failures
set -euo pipefail
# run-tests.sh
# This script runs the test suite for the codebase and checks coverage.
# pytest options (coverage source, threshold, report format) are configured in pyproject.toml.
#
# Usage:
#   bash scripts/run-tests.sh [TEST_DIR]
#
# Arguments:
#   TEST_DIR   Directory containing test files (default: /app/tests)
#
# Example:
#   bash scripts/run-tests.sh tests

# Use argument if provided, otherwise default to Docker path
TEST_DIR="${1:-/app/tests}"

echo "Running tests..."
uv run pytest "${TEST_DIR}"
