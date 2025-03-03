import chromadb
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from chromadb import PersistentClient
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()
# Kết nối tới ChromaDB
client = PersistentClient(path="./chroma_db")

vectorstore = Chroma(client=client, collection_name="langchain", embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # Trả về 5 tài liệu liên quan nhất

# 4. Pipeline RAG hoàn chỉnh
def rag_pipeline(user_message:str):
    # Kết nối ChromaDB
    client = PersistentClient(path="./chroma_db")
    vectorstore = Chroma(client=client, collection_name="langchain", embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # Truy vấn 5 tài liệu liên quan nhất

    # Lấy tài liệu từ ChromaDB
    docs = retriever.invoke(user_message)

    # Định dạng tài liệu thành một chuỗi context
    context = "\n\n".join(doc.page_content for doc in docs)

    # Prompt Template
    template = """Bạn là một trợ lý AI thông minh, thân thiện và giao tiếp tự nhiên như con người. Hãy phản hồi giống như một người bạn đang trò chuyện, sử dụng ngôn ngữ tự nhiên, thân thiện, và tránh quá cứng nhắc.    
    - Sử dụng câu ngắn gọn, tự nhiên.  
    - Nếu câu hỏi không rõ, hãy hỏi lại thay vì giả định sai.  
    - Đừng lặp lại câu từ cứng nhắc từ câu hỏi.  

    Context:
    {context}
    
    Question: {question}"""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # LLM
    # llm = ChatOpenAI(model_name="gpt-4", temperature=0.6)
    llm = ChatOpenAI(model_name= os.getenv("MODEL_OPENAI_NAME"), temperature=0.6)

    # Chain
    rag_chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    # Nhập context và câu hỏi vào chain
    answer = rag_chain.invoke({"context": context, "question": user_message})
    return answer.content
