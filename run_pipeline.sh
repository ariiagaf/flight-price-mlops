#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$PROJECT_DIR/.venv/bin/python"

export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

cd "$PROJECT_DIR"

echo "=== Stage 1: Data Engineering ==="
"$PYTHON" code/datasets/preprocess.py

echo "=== Stage 2: Model Engineering ==="
"$PYTHON" code/models/train.py

echo "=== Stage 3: Deployment ==="
docker compose -f code/deployment/docker-compose.yml restart api

echo "=== Pipeline completed successfully ==="
