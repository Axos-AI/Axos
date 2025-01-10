import mimetypes
import os
import uuid
from fastapi import UploadFile

from src.sdk.exceptions import FileTypeNotFoundError, InvalidFileTypeError

async def save_upload_file_temp(upload_file: UploadFile) -> str:
    """
    Save an UploadFile to a temporary location and return the path.
    
    Args:
        upload_file (UploadFile): The uploaded file from FastAPI
        
    Returns:
        str: Path to the temporary file
    """
    # Generate unique filename with original extension if it exists
    original_filename = upload_file.filename or "upload"
    file_extension = os.path.splitext(original_filename)[1]
    temp_filename = f"{uuid.uuid4()}{file_extension}"
    temp_file_path = os.path.join("/tmp", temp_filename)
    
    # Save the uploaded file
    with open(temp_file_path, "wb") as buffer:
        content = await upload_file.read()
        buffer.write(content)
    
    return temp_file_path 

def delete_file(file_path: str):
    """
    Delete a file from the filesystem.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


# List of accepted video mime types by Google Gemini API
ACCEPTED_MIME_TYPES = [
    'video/mp4',
    'video/mpeg',
    'video/mov',
    'video/avi',
    'video/x-flv',
    'video/mpg',
    'video/webm',
    'video/wmv',
    'video/3gpp',
]

def validate_file_type(file_path: str) -> bool:
    
    file_type = guess_file_type(file_path)
    if file_type is None:
        raise FileTypeNotFoundError(f"Failed to guess file type for {file_path}")
    if not is_valid_file_type(file_type):
        raise InvalidFileTypeError(f"Invalid file type: {file_type}")
    return True

def is_valid_file_type(file_type: str) -> bool:
    return file_type in ACCEPTED_MIME_TYPES

def guess_file_type(file_path: str) -> str | None:
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type
