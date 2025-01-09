"""This module contains the API endpoints for the application."""

import json
from typing import List
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, Body, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse
import time
import uuid

from src.core.async_worker import celery, interpret, gauge_prompt_adherance
from src.utils.dependencies import validate_token
from src.utils.file_handling import save_upload_file_temp

router = APIRouter()


# List of accepted video mime types
ACCEPTED_MIME_TYPES = [
    'video/mp4',
    'video/mpeg',
    'video/quicktime',
    'video/x-msvideo',
    'video/x-ms-wmv',
    'video/webm',
    'application/octet-stream'
]



@router.get("/health")
async def health():
    """
    Health check endpoint.
    Returns:
        JSONResponse: Returns {"text": "OK"} if the service is running.
    """
    return JSONResponse({"text": "OK"})

@router.post("/interpret")
async def interpret_task(video: UploadFile = File(...)):
    """
    Interpret a video.
    Returns:
        JSONResponse: Returns {"status": "processing", "task_id": task.id} while the task is processing.
    """
    if video.content_type not in ACCEPTED_MIME_TYPES:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid file type",
                "message": f"File must be a video. Received: {video.content_type}",
                "accepted_types": ACCEPTED_MIME_TYPES
            }
        )

    temp_file_path = await save_upload_file_temp(video)
    task = interpret.delay(temp_file_path)
    return JSONResponse({"status": "processing", "task_id": task.id})

@router.post("/gauge_prompt_adherance")
async def gauge_prompt_adherance_task(video: UploadFile = File(...), prompt: str = Body(...)):
    """
    Video report endpoint.
    Returns:
        JSONResponse: Returns {"status": "processing", "task_id": task.id} while the task is processing.
    """
    if video.content_type not in ACCEPTED_MIME_TYPES:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid file type",
                "message": f"File must be a video. Received: {video.content_type}",
                "accepted_types": ACCEPTED_MIME_TYPES
            }
        )

    temp_file_path = await save_upload_file_temp(video)
    task = gauge_prompt_adherance.delay(temp_file_path, prompt)
    return JSONResponse({"status": "processing", "task_id": task.id})

@router.get("/task_status")
async def task_status(task_id: str):
    """
    Get the status of a task.
    Returns:
        JSONResponse: Returns task status and result/error information
    """
    task_async_result = AsyncResult(task_id, app=celery)

    if task_async_result.ready():
        try:
            # Get the result, but handle potential errors
            result = task_async_result.get()
            return JSONResponse({
                "status": "complete",
                "result": result
            })
        except Exception as e:
            # Handle any errors that occurred during task execution
            return JSONResponse({
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__
            }, status_code=500)
    else:
        return JSONResponse({"status": "processing"})