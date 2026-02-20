import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "api_key")
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL_NAME = "google/gemini-3-flash-preview"
    APP_TITLE = "CaloriSense API"

settings = Config()
