#!/bin/sh

# Set the path to the virtual environment
VENV_PATH="/Axos/venv/bin/activate"

# Set the path to the backend working directory
WORKDIR_PATH="/Axos/odyssey"

# Check if the virtual environment exists
if [ ! -f "$VENV_PATH" ]; then
  echo "Virtual environment activation script not found at $VENV_PATH"
  exit 1
fi

# Activate the virtual environment
. "$VENV_PATH"

# Check if the working directory exists
if [ ! -d "$WORKDIR_PATH" ]; then
  echo "Working directory not found at $WORKDIR_PATH"
  exit 1
fi

# Navigate to the backend working directory
cd "$WORKDIR_PATH"

# Start the services
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload &
celery -A src.core.celery_worker worker --loglevel=info --pool=threads
# celery -A src.core.celery_worker worker --loglevel=info --pool=threads &
# celery -A src.core.celery_worker beat --loglevel=info

# Wait indefinitely to keep the container running
tail -f /dev/null
