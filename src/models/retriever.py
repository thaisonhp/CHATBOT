from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

class ChromaRetriever:
    def __init__(self, documents, embedding_model=None):
        """
        Khởi tạo vectorstore từ danh sách tài liệu và tạo retriever.

        :param documents: Danh sách các Document đã được xử lý (splits).
        :param embedding_model: Mô hình embedding để chuyển đổi văn bản thành vector.
        """
        self.embedding_model = embedding_model or OpenAIEmbeddings()
        self.vectorstore = Chroma.from_documents(documents=documents, embedding=self.embedding_model)
        self.retriever = self.vectorstore.as_retriever()

    def get_retriever(self):
        """
        Trả về retriever để sử dụng trong quá trình truy vấn.
        """
        return self.retriever

    def query(self, query_text, k=5):
        """
        Truy vấn tài liệu liên quan từ vectorstore.

        :param query_text: Câu truy vấn của người dùng.
        :param k: Số lượng tài liệu muốn truy xuất.
        :return: Danh sách các tài liệu liên quan.
        """
        return self.retriever.get_relevant_documents(query_text, k=k)
