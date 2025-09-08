#!/bin/sh
set -e

# echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting Uvicorn..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000