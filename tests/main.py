from chromadb import PersistentClient

try:
    # Kết nối đến ChromaDB
    client = PersistentClient(path="/Users/luongthaison/Documents/Third_years_student/Project/CHAT_BOT/chroma_db")  
    collections = client.list_collections()  # Chỉ lấy danh sách tên collections
    print("Danh sách collections trước khi xóa:", collections)

    # Xóa collection "langchain" nếu tồn tại
    collection_name = "langchain"
    
    if collection_name in collections:
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' đã bị xóa.")
    else:
        print(f"Collection '{collection_name}' không tồn tại.")

    print("Danh sách collections sau khi xóa:", client.list_collections())

except Exception as e:
    print("Lỗi kết nối ChromaDB:", e)
