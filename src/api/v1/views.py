"""This module contains the API endpoints for the application."""

import json
from typing import List
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, Body, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse
import time
import uuid

from core.async_worker import celery, interpret, guage_prompt_adherance
from utils.dependencies import validate_token
from src.utils.file_handling import save_upload_file_temp

router = APIRouter()




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
    temp_file_path = await save_upload_file_temp(video)
    task = interpret.delay(temp_file_path)
    return JSONResponse({"status": "processing", "task_id": task.id})


@router.post("/guage_prompt_adherance")
async def guage_prompt_adherance_task(video: UploadFile = File(...), prompt: str = Body(...)):
    """
    Video report endpoint.
    Returns:
        JSONResponse: Returns {"status": "processing", "task_id": task.id} while the task is processing.
    """
    task = guage_prompt_adherance.delay(video.file.name, prompt)
    return JSONResponse({"status": "processing", "task_id": task.id})

@router.get("/task_status")
async def task_status(task_id: str):
    """
    Get the status of a task.
    Returns:
        JSONResponse: Returns {"status": "complete", "result": result} if the task is complete.
    """
    task_async_result = AsyncResult(task_id, app=celery)

    if task_async_result.ready():
        # Retrieve the result of the task
        result = task_async_result.result
        return JSONResponse({"status": "complete", "result": result})
    else:
        return JSONResponse({"status": "processing"})