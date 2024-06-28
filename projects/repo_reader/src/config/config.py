#config.py
import os
from dotenv import load_dotenv

WHITE = "\033[37m"
GREEN = "\033[32m"
RESET_COLOR = "\033[0m"
model_name = "gpt-4o"

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
