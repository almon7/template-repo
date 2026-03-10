#!/bin/bash
# -e: abort on error  -u: error on unset variables  -o pipefail: propagate pipe failures
set -euo pipefail
# dev-entrypoint.sh
# This script is executed when the dev Docker container starts.

uv run python -m app.main