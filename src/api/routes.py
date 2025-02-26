from fastapi import APIRouter ,UploadFile , File 
# from src.services.query_handler import QueryHandler
from src.api.schemas import QueryRequest, QueryResponse
from io import BytesIO
from models.indexing import load_pdf_from_file
from services.process_pdf import process_documents
router = APIRouter()

@router.post("/chat", response_model=QueryResponse)
def chat(query: QueryRequest):
    return QueryResponse(response=f"Bạn đã gửi: {query.text}")



@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """API nhận tệp PDF, chuyển thành list[Document]"""
    pdf_file = BytesIO(await file.read())  # Đọc file từ request
    docs = load_pdf_from_file(pdf_file)  # Chuyển thành Document
    retriver = process_documents(documents=docs) # # split va embedd vao db 
    return {"total_pages": len(docs), "documents": [doc.page_content[:200] for doc in docs]}  
    # Trả về số trang và nội dung 200 ký tự đầu tiên của mỗi trang

