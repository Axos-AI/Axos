"""This module contains the API endpoints for the application."""

import json
from typing import List
from celery import uuid
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, Body, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse
import time
import uuid

from core.celery_worker import celery
from utils.dependencies import validate_token

router = APIRouter()




@router.get("/health")
async def health():
    """
    Health check endpoint.
    Returns:
        JSONResponse: Returns {"text": "OK"} if the service is running.
    """
    return JSONResponse({"text": "OK"})



def return_task(task):
    # Loop until the task is complete
    while True:
        task_async_result = AsyncResult(task.id, app=celery)
        task_status = task_async_result.status

        if task_status == "SUCCESS":
            # Retrieve the result of the task
            result = task_async_result.result
            return JSONResponse({"status": "complete", "result": result})
        elif task_status == "FAILURE":
            # Retrieve the exception info
            result = task_async_result.result
            return JSONResponse({"status": "error", "result": result})
        else:
            # Sleep for a short duration before checking again to avoid busy waiting
            time.sleep(1)
            continue