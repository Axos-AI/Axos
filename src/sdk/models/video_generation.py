from pydantic import BaseModel

# Fake Sora API model
class VideoGenerationRequest(BaseModel):
    prompt: str
    model: str = "sora-1.0-turbo"
    size: str = "1920x1080"

class VideoGenerationResponse(BaseModel):
    url: str
    revised_prompt: str = ""
