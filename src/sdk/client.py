import os
import time
import requests

from src.sdk.exceptions import APIError, TaskError, TaskFailedError, ValidationError, VideoNotFoundError

# SDK can internally use the API server for processing
class ShardClient:
    def __init__(self, api_key: str, api_url="http://localhost:8000/v1"):
        self.api_key = api_key
        self.api_url = api_url
    
    def interpret(self, video_path: str):
        # Option 1: Use API server

        headers = {
            # "Authorization": f"Bearer {self.api_key}"
        }
        try:
            with open(video_path, 'rb') as f:
                if os.path.getsize(video_path) == 0:
                    raise VideoNotFoundError("File is empty")
                files = {'video': f}
                response = requests.post(f"{self.api_url}/interpret", files=files, headers=headers)

                if response.status_code != 200:
                    raise APIError(f"Error: {response.json().get('error', 'Unknown error')}")
                task_id = response.json()['task_id']
                while True:
                    task_response = requests.get(f"{self.api_url}/task/{task_id}", headers=headers)
                    if task_response.status_code != 200:
                        raise TaskError(f"Error: {task_response.json().get('error', 'Unknown error')}")
                    if task_response.json().get('status') == 'failed':
                        raise TaskFailedError(f"Error: {task_response.json().get('error', 'Unknown error')}")
                    if task_response.json().get('status') == 'complete':
                        return task_response.json().get('result')
                    time.sleep(5)
            
        except Exception as e:
            raise e
        
            
        # Option 2: Direct processing
        # Implement direct processing logic here


