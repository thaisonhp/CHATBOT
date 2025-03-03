from chromadb import PersistentClient

try:
    client = PersistentClient(path="/Users/luongthaison/Documents/Third_years_student/Project/CHAT_BOT/chroma_db")  # Thay bằng đường dẫn của bạn
    print(client.list_collections())  # Kiểm tra danh sách collections
except Exception as e:
    print("Lỗi kết nối ChromaDB:", e)

collection = client.get_collection("langchain")  # Thay bằng tên collection
print(collection.count())  # Kiểm tra số lượng vector lưu trong DB

