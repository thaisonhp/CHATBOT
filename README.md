# Chatbot RAG (Retrieval-Augmented Generation)

## 🚀 Giới thiệu
Chatbot RAG là hệ thống chatbot thông minh kết hợp giữa truy xuất thông tin và mô hình sinh văn bản để tạo ra phản hồi chính xác, tự nhiên hơn. Hệ thống sử dụng **FastAPI** làm backend, **FAISS** hoặc **ChromaDB** để lưu trữ vector dữ liệu, và mô hình ngôn ngữ lớn (LLM) để sinh câu trả lời.

## 📂 Cấu trúc thư mục
```
chatbot-rag/
│── src/
│   ├── api/                  # API endpoints (FastAPI)
│   │   ├── __init__.py
│   │   ├── routes.py         # Xử lý request
│   │   ├── schemas.py        # Định nghĩa request/response model
│   ├── core/                 # Cấu hình chính
│   │   ├── config.py         # Config chung (API keys, DB, model paths,...)
│   │   ├── dependencies.py   # Dependency Injection (DI)
│   ├── database/             # Lưu trữ và truy vấn dữ liệu
│   │   ├── __init__.py
│   │   ├── vector_store.py   # Quản lý vector database (FAISS, ChromaDB,...)
│   ├── models/               # Xử lý các model ML/NLP
│   │   ├── __init__.py
│   │   ├── retriever.py      # Tìm kiếm dữ liệu
│   │   ├── generator.py      # Mô hình sinh văn bản (LLM)
│   ├── services/             # Xử lý nghiệp vụ chatbot
│   │   ├── __init__.py
│   │   ├── query_handler.py  # Kết hợp retriever & generator
│   │   ├── response_builder.py  # Xây dựng response
│   ├── utils/                # Các hàm tiện ích
│   │   ├── __init__.py
│   │   ├── logger.py         # Logging
│   │   ├── text_processing.py  # Tiền xử lý văn bản
│   ├── main.py               # Chạy ứng dụng
│── tests/                    # Unit tests
│── configs/                  # Cấu hình môi trường
│── Dockerfile                # Docker config
│── requirements.txt          # Dependencies
│── README.md                 # Hướng dẫn sử dụng
```

## 🔧 Cài đặt
### 1️⃣ Yêu cầu hệ thống
- Python 3.8+
- Pipenv hoặc Virtualenv (khuyến nghị)
- Docker (tuỳ chọn)

### 2️⃣ Cài đặt môi trường ảo
```bash
python -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)
```

### 3️⃣ Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Tạo file `.env`
Tạo file `.env` trong thư mục gốc với nội dung:
```ini
MODEL_NAME=gpt-4
VECTOR_DB_PATH=data/vector_store
OPENAI_API_KEY=your_openai_api_key_here
TOP_K=5
HOST=0.0.0.0
PORT=8000
```

## 🚀 Chạy ứng dụng
### 1️⃣ Chạy bằng FastAPI
```bash
uvicorn src.main:app --host $(grep HOST .env | cut -d '=' -f2) --port $(grep PORT .env | cut -d '=' -f2) --reload
```
Sau khi chạy, API có thể truy cập tại: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2️⃣ Chạy bằng Docker (tuỳ chọn)
```bash
docker build -t chatbot-rag .
docker run -p 8000:8000 --env-file .env chatbot-rag
```

## 📌 API Endpoints
| Phương thức | Endpoint      | Mô tả                           |
|------------|--------------|--------------------------------|
| `POST`    | `/chat`       | Nhận câu hỏi từ người dùng    |
| `GET`     | `/health`     | Kiểm tra trạng thái server    |

## 🔍 Kiến trúc RAG
- **Retriever**: Truy vấn dữ liệu từ FAISS/ChromaDB dựa trên embedding vector.
- **Generator**: Sử dụng mô hình LLM (GPT-4, Llama, hay HuggingFace) để sinh phản hồi.
- **Pipeline**: Kết hợp cả hai để tạo ra câu trả lời tối ưu.

## 📜 Giấy phép
Dự án này được phát hành dưới giấy phép MIT. Bạn có thể sử dụng, chỉnh sửa và phát triển tiếp theo.

---
💡 *Đóng góp hoặc báo lỗi tại GitHub!* 🚀

