from typing import List
import re
def clean_text(text: str) -> str:
    """Loại bỏ ký tự đặc biệt và chuẩn hóa văn bản."""
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower().strip()

def tokenize(text: str) -> List[str]:
    """Tách từ thành danh sách tokens."""
    return text.split()

def preprocess_text(text: str) -> List[str]:
    """Tiền xử lý tổng hợp gồm làm sạch và tokenization."""
    return tokenize(clean_text(text))