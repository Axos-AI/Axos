class APIError(Exception):
    """Raised when there is an error with the API request."""

class ValidationError(Exception):
    """Raised for invalid data inputs."""

class TaskError(Exception):
    """Raised when there is an error with the task request."""

class TaskFailedError(Exception):
    """Raised when the task request fails."""

class VideoNotFoundError(Exception):
    """Raised when the video is not found."""

class VideoProcessingError(Exception):
    """Raised when the video processing fails."""

class FileTypeNotFoundError(Exception):
    """Raised when the file type is not found."""

class InvalidFileTypeError(Exception):
    """Raised when the file type is not valid."""

