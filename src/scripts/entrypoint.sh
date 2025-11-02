#!/bin/bash
# entrypoint.sh
# This script is executed when the Docker container starts.

uv run jupyter notebook --port 8888 --no-browser --ip=0.0.0.0 --notebook-dir app/
