from rank_bm25 import BM25Okapi
import numpy as np
from langchain_openai import OpenAIEmbeddings
import os 
import chromadb

# Khởi tạo client và collection
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Đường dẫn database
collection = chroma_client.get_or_create_collection(name="langchain")

def get_documents():
    """Lấy danh sách tài liệu từ ChromaDB"""
    results = collection.get(include=["documents", "metadatas"])  # Lấy cả metadata nếu cần
    return results["documents"], results["metadatas"]

# Lấy danh sách tài liệu từ database
documents, metadatas = get_documents()
tokenized_corpus = [doc.split(" ") for doc in documents]
bm25 = BM25Okapi(tokenized_corpus)

def hybrid_search(query, embedding_model=None, top_k=5, alpha=0.5):
    """Kết hợp BM25 và Vector Search để cải thiện kết quả truy xuất"""
    if embedding_model is None:
        embedding_model = OpenAIEmbeddings()  # Sử dụng OpenAIEmbeddings mặc định

    # 1️⃣ BM25 Search
    tokenized_query = query.split(" ")
    bm25_scores = bm25.get_scores(tokenized_query)

    # 2️⃣ Vector Search từ ChromaDB
    query_embedding = embedding_model.embed_query(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    # Lấy danh sách ID từ ChromaDB
    retrieved_ids = results.get("ids", [[]])[0]  # Tránh lỗi nếu không có kết quả
    retrieved_distances = results.get("distances", [[]])[0]  

    # 3️⃣ Kết hợp điểm BM25 + Vector Search
    bm25_scores = np.array(bm25_scores)
    bm25_ranks = np.argsort(-bm25_scores)[:top_k]

    hybrid_results = {}
    all_doc_ids = collection.get()["ids"]  # Lấy danh sách ID từ ChromaDB

    for idx, doc_id in enumerate(retrieved_ids):
        if doc_id in all_doc_ids:
            doc_index = all_doc_ids.index(doc_id)  # Lấy index của doc_id
            hybrid_score = alpha * bm25_scores[doc_index] + (1 - alpha) * retrieved_distances[idx]
            hybrid_results[doc_id] = hybrid_score
        else:
            print(f"⚠️ Warning: doc_id {doc_id} không tìm thấy trong collection.")

    sorted_results = sorted(hybrid_results.items(), key=lambda x: x[1], reverse=True)
    
    return [documents[all_doc_ids.index(idx)] for idx, _ in sorted_results if idx in all_doc_ids]

# Test tìm kiếm với Hybrid Search
embedding_model = OpenAIEmbeddings()
query = "Lương Thái Sơn là ai?"
retrieved_docs = hybrid_search(query, embedding_model)
print("🔍 Kết quả truy xuất:", retrieved_docs)
