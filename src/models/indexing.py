from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import fitz  # PyMuPDF
from langchain.schema import Document

def load_pdf_from_file(file: BytesIO):
    """Chuyển tệp PDF thành danh sách Document."""
    doc = fitz.open(stream=file.read(), filetype="pdf")  # Mở PDF từ bộ nhớ
    documents = []

    for page in doc:
        text = page.get_text("text")  # Lấy nội dung trang
        documents.append(Document(page_content=text, metadata={"page": page.number}))
    
    return documents