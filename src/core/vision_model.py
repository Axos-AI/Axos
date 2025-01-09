from markdown import Markdown
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Choose a Gemini model.
model = genai.GenerativeModel(model_name="gemini-1.5-pro")


# Create the prompt.
interpret_video_prompt = "Summarize this video."
gauge_prompt_adherance_prompt = "Summarize this video. Then determine if the given prompt aligns with the video:"


def upload_video(video_path: str):
    """Upload a video to the model."""
    video_file = genai.upload_file(path=video_path)

    # Check whether the file is ready to be used.
    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)
    return video_file


def interpret_video(video_path: str, model_prompt: str = interpret_video_prompt):
    """Interpret a video."""
    video_file = upload_video(video_path)

    
    # Make the LLM request.
    print("Making LLM inference request...")
    response = model.generate_content([video_file, model_prompt],
                                    request_options={"timeout": 600})
    video_file.delete()
    # Print the response, rendering any Markdown
    # Markdown(response.text)
    return response.text

def gauge_video_prompt_adherance(video_path: str, user_prompt: str, model_prompt: str = gauge_prompt_adherance_prompt):
    """Gauge prompt adherance."""
    video_file = upload_video(video_path)
    final_prompt = f"{model_prompt} {user_prompt}"
    response = model.generate_content([video_file, final_prompt],
                                    request_options={"timeout": 600})
    video_file.delete()
    # Markdown(response.text)
    return response.text
