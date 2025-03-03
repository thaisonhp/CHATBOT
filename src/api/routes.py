from fastapi import APIRouter ,UploadFile , File 
# from src.services.query_handler import QueryHandler
from src.api.schemas import QueryRequest, QueryResponse
from io import BytesIO
from models.indexing import load_pdf_from_file
from services.process_pdf import process_documents
from services.retrivaler import rag_pipeline
from fastapi import HTTPException

router = APIRouter()

@router.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    user_message = request.text  # Lấy giá trị từ request JSON

    if not isinstance(user_message, str):
        raise ValueError("Lỗi: user_message phải là một chuỗi (str)")
    print(f"user_message type: {type(user_message)}, value: {user_message}")
    answer = rag_pipeline(user_message)
    return QueryResponse(response=f"Kết quả là: {answer}")

    
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



