from src.models.generator import TextGenerator
from src.models.retriever import Retriever

class ResponseBuilder:
    def __init__(self, retriever: Retriever, generator: TextGenerator):
        self.retriever = retriever
        self.generator = generator

    def build_response(self, query: str):
        """Kết hợp dữ liệu truy xuất và mô hình sinh để tạo phản hồi."""
        retrieved_docs = self.retriever.search(query)
        context = "\n".join(retrieved_docs) if isinstance(retrieved_docs, list) else retrieved_docs
        return self.generator.generate(query, context)