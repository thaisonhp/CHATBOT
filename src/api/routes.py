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
    # bước 1 : load doc 
    docs = process_file(file) # lấy ra văn bản text , thông số ... 
    # Bước 2 : phân loại tài liệu để áp dụng các phương pháp chunk phù hợp 
     
    # bước 3 : chunking 
    chunker = TextChunker(method='semantic') 
    doc_chunked  = chunker.chunk(docs) # doc_chunked : List[str] 
    # bước 4 : embeding 
    embedder = Embedder()
    text_embedded = embedder.embed_text(doc_chunked) # List[float]
    # bước 5 : lưu vào chroma db 
    indexer = ChromaDBIndexer(collection_name="langchain")
    indexer.add_texts(text_embedded, ids)
    response_data = {"status": "success", "message": "Tải file thành công!"}
    return response_data




