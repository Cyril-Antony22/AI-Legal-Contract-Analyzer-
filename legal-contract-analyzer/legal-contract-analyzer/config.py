import os
from dotenv import load_dotenv

# Load variables from a .env file into the environment
load_dotenv()

class Config:
    # ---- Folders ----
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    REPORT_FOLDER = os.path.join(os.getcwd(), "reports")
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

    # ---- OpenRouter (Generative AI) settings ----
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    # You can swap this for any model available on https://openrouter.ai/models
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    # ---- Flask ----
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit
