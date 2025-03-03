from fastapi import FastAPI
from src.api.routes import router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Chatbot RAG API")

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn gốc
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức (GET, POST, OPTIONS...)
    allow_headers=["*"],  # Cho phép tất cả header
)


def start():
    """Hàm khởi chạy FastAPI."""
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, log_level="debug")

if __name__ == "__main__":
    start()
