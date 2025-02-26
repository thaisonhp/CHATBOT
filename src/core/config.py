import os
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

class Config:
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "data/vector_store")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
    TOP_K = int(os.getenv("TOP_K", 5))
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
