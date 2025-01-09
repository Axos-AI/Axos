import os
import uuid
from fastapi import UploadFile

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