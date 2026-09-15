#!/bin/bash

set -e

echo "=== Stage 1: Data Engineering ==="
python code/datasets/preprocess.py

echo "=== Stage 2: Model Engineering ==="
python code/models/train.py

echo "=== Stage 3: Deployment ==="
docker compose -f code/deployment/docker-compose.yml restart api

echo "=== Pipeline completed successfully ==="