"""This module contains the Celery worker tasks for the Supplier Outbound service."""

import os
import threading
from celery import Celery
from src.core.vision_model import interpret_video
from src.utils.file_handling import delete_file

CHECK_EMAIL_LOCK = threading.Lock()

# Set default values for Redis configuration
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")  # Default Redis port

if REDIS_HOSTNAME == "localhost":
    celery = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
else:
    # we're using a hosted redis and need TLS enabled
    celery = Celery(
        "tasks",
        broker=f"rediss://{REDIS_HOSTNAME}:{REDIS_PORT}/0?ssl_cert_reqs=CERT_REQUIRED",
        backend=f"rediss://{REDIS_HOSTNAME}:{REDIS_PORT}/0?ssl_cert_reqs=CERT_REQUIRED",
    )

@celery.task
def interpret(video_path: str):
    """Interpret a video."""
    try:
        # Process the video file here
        # Your video processing code goes here
        result = interpret_video(video_path)
        return result
    finally:
        # Clean up the temporary file
        delete_file(video_path)

@celery.task
def guage_prompt_adherance(video_path: str, prompt: str):
    """Gauge prompt adherance."""
    try:
        # Process the video file here
        # Your video processing code goes here
        result = guage_prompt_adherance(video_path, prompt)
        return result
    finally:
        # Clean up the temporary file
        delete_file(video_path)

if __name__ == "__main__":
    options = {
        "loglevel": "INFO",
        "traceback": True,
    }

    celery.Worker(pool_cls="threads", **options).start()
