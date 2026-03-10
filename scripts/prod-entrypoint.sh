#!/bin/bash
# -e: abort on error  -u: error on unset variables  -o pipefail: propagate pipe failures
set -euo pipefail
# prod-entrypoint.sh
# This script is executed when the production Docker container starts.

uv run python -m app.main