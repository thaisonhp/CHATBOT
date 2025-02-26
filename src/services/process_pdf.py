from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def process_documents(documents, embedding_model=None):
    """
    Xử lý tài liệu: chia nhỏ và lưu vào ChromaDB.

    :param documents: Danh sách tài liệu (list[Document]).
    :param embedding_model: Mô hình embedding để chuyển đổi văn bản (mặc định OpenAIEmbeddings).
    :return: retriever để tìm kiếm tài liệu liên quan.
    """
    # Bước 1: Chia nhỏ tài liệu
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(documents)

    # Bước 2: Lưu vào ChromaDB
    embedding_model = embedding_model or OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(splits, embedding=embedding_model)

    # Bước 3: Trả về retriever
    return vectorstore.as_retriever()
