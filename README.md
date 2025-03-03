# Chatbot RAG (Retrieval-Augmented Generation)

## 🚀 Giới thiệu
Chatbot RAG là hệ thống chatbot thông minh kết hợp giữa truy xuất thông tin và mô hình sinh văn bản để tạo ra phản hồi chính xác, tự nhiên hơn. Hệ thống sử dụng **FastAPI** làm backend, **ChromaDB** để lưu trữ vector dữ liệu, và mô hình ngôn ngữ lớn (LLM) để sinh câu trả lời.


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
|------------|---------------|----------------------------------|
| `POST`    | `/chat`        | Nhận câu hỏi từ người dùng       |
| `POST`     | `/upload-pdf/`| Tải tiều liệu lên server         |

## 🔍 Kiến trúc RAG
- **Retriever**: Truy vấn dữ liệu từ FAISS/ChromaDB dựa trên embedding vector.
- **Generator**: Sử dụng mô hình LLM (GPT-4, Llama, hay HuggingFace) để sinh phản hồi.
- **Pipeline**: Kết hợp cả hai để tạo ra câu trả lời tối ưu.

## 📜 Giấy phép
Dự án này được phát hành dưới giấy phép MIT. Bạn có thể sử dụng, chỉnh sửa và phát triển tiếp theo.

---
💡 *Đóng góp hoặc báo lỗi tại GitHub!* 🚀

