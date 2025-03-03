from fastapi import APIRouter ,UploadFile , File
# from src.services.query_handler import QueryHandler
from src.api.schemas import QueryRequest, QueryResponse
from io import BytesIO
from models.indexing import load_pdf_from_file
from services.process_pdf import process_documents
from services.retrivaler import rag_pipeline
from fastapi import HTTPException 
from fastapi.responses import StreamingResponse

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

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    print(f"📂 Đọc được {len(contents)} bytes từ PDF")

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Lỗi đọc file! File có thể bị hỏng.")

    pdf_file = BytesIO(contents)  
    docs = load_pdf_from_file(pdf_file)  
    print(f"📄 Số trang đọc được: {len(docs)}")
    
    retriever = process_documents(documents=docs)
    return retriever



