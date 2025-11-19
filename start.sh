#!/bin/bash
# start.sh

# Wait for PostgreSQL to be ready on port 5432
echo "Waiting for PostgreSQL..."
/bin/bash -c 'while ! nc -z db 5432; do sleep 1; done'
echo "PostgreSQL is available."

# Wait for Ollama to be ready on port 11434
echo "Waiting for Ollama..."
# We wait for the port, but the model may still be downloading/loading.
/bin/bash -c 'while ! nc -z ollama 11434; do sleep 1; done'
echo "Ollama service is available. Starting FastAPI..."

# Manually pull the model if it's not already downloaded
# This command relies on the 'ollama' CLI being accessible from the host/docker network, 
# which it is, but it's cleaner to handle model pull externally if possible.
# Since we can't reliably pull from inside the API container, we rely on the user
# to ensure the model is pulled or wait for the API to retry.

# Run database migrations (optional, but good practice)
# echo "Running Alembic migrations..."
# alembic upgrade head

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000