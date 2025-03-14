from fastapi import APIRouter ,UploadFile , File
# from src.services.query_handler import QueryHandler
from src.api.schemas import QueryRequest, QueryResponse
from io import BytesIO
from services.indexing import process_file
from services.pipeline import rag_pipeline
from fastapi import HTTPException 
from fastapi.responses import StreamingResponse
from utils.process_pdf import process_pdf
from services.indexing import TextChunker
from services.share import Embedder , ChromaDBIndexer
from hashlib import md5

router = APIRouter()


@router.post("/chat")
async def chat(request: QueryRequest):
    user_message = request.text

    if not isinstance(user_message, str):
        raise HTTPException(status_code=400, detail="Lỗi: user_message phải là một chuỗi (str)")

    if not user_message.strip():  # Kiểm tra rỗng
        raise HTTPException(status_code=400, detail="Lỗi: user_message không được để trống")

    async def generate():
        try:
            async for chunk in rag_pipeline(user_message):  # Dùng async for
                yield str(chunk)
        except Exception as e:
            yield f"Lỗi khi xử lý yêu cầu: {str(e)}"

    return StreamingResponse(generate(), media_type="text/plain")


    
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
from fastapi.responses import JSONResponse

@router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    """
    API nhận file tải lên và xử lý nội dung.

    Args:
        file (UploadFile): File tải lên từ người dùng.

    Returns:
        dict: Kết quả xử lý file.
    """
    # Bước 1: Load nội dung tài liệu
    docs = process_file(file)  # Lấy văn bản từ file

    # Bước 2: Chia nhỏ tài liệu (Chunking)
    chunker = TextChunker(method='semantic')
    doc_chunked = chunker.chunk(docs)  # List[str]

    if not doc_chunked:
        raise HTTPException(status_code=400, detail="Không tìm thấy nội dung hợp lệ sau khi chia nhỏ.")

    # Bước 3: Tạo IDs cho từng đoạn văn bản
    ids = [md5(text.encode()).hexdigest() for text in doc_chunked]

    # Bước 4: Chuyển văn bản thành vector embeddings
    embedder = Embedder()
    text_embedded = embedder.embed_text(doc_chunked)  # List[list[float]]

    # Bước 5: Lưu vào ChromaDB
    indexer = ChromaDBIndexer(collection_name="langchain")
    indexer.add_texts(doc_chunked, text_embedded, ids)

    return JSONResponse(content={"status": "success", "message": "Tải file thành công!"})




