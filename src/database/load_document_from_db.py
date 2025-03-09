import chromadb

# Khởi tạo client và collection
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Đường dẫn database
collection = chroma_client.get_or_create_collection(name="langchain")

def get_documents():
    """Lấy danh sách tài liệu từ ChromaDB"""
    results = collection.get(include=["documents"])
    return results["documents"]
