from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import hub

class RAGGenerator:
    def __init__(self, documents, model_name="gpt-4", temperature=0):
        """
        Khởi tạo hệ thống RAG (Retrieval-Augmented Generation).
        
        - `documents`: Danh sách tài liệu đầu vào.
        - `model_name`: Tên mô hình OpenAI sử dụng.
        - `temperature`: Nhiệt độ của mô hình, ảnh hưởng đến tính sáng tạo của đầu ra.
        """
        # Tạo vectorstore từ tài liệu và tạo retriever
        self.vectorstore = Chroma.from_documents(documents=documents, embedding=OpenAIEmbeddings())
        self.retriever = self.vectorstore.as_retriever()
        
        # Load prompt từ LangChain Hub (hoặc dùng prompt custom)
        self.prompt = hub.pull("rlm/rag-prompt")  # Thay bằng prompt tùy chỉnh nếu cần
        
        # Khởi tạo mô hình GPT
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        
        # Xây dựng pipeline xử lý
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def generate_answer(self, question):
        """
        Nhận câu hỏi từ người dùng và tạo câu trả lời bằng RAG.
        """
        return self.chain.invoke(question)

# ======== CÁCH SỬ DỤNG ==========
# Giả sử bạn đã có danh sách tài liệu `docs`
# rag = RAGGenerator(documents=docs)
# response = rag.generate_answer("What is Task Decomposition?")
# print(response)
