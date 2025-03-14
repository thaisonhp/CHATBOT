import chromadb
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from chromadb import PersistentClient
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from services.share import ChromaDBIndexer
from services.pre_retrival import generate_queries
import os

load_dotenv()

# 4. Pipeline RAG hoàn chỉnh
async def rag_pipeline(user_message: str):

     # Bước bổ sung : 
    """
    1. Thêm query rewriting 
    2. Thêm query explansion  
    3 . Generate query 
    """

    query_generated = generate_queries.invoke(user_message)

    # Bước 1 : truy vấn câu hỏi của người dùng trong db (Bước này là Retrieval)
    indexer = ChromaDBIndexer(collection_name="langchain")
    query_connected = ""
    for query in query_generated : 
        query_connected += query
    
    context = indexer.query(query_connected)
    # Bước bổ sung Post-Retrieval 
    """
    1. Rerank 
    2. Summary 
    3. Fusion 
    """
    # Bước 2 : viết Prompt Template 

    template = """Bạn là một trợ lý AI thông minh của câu lạc bộ tin học HIT của trường đại học Công nghiệp Hà Nội, thân thiện và giao tiếp tự nhiên như con người. Hãy phản hồi giống như một người bạn đang trò chuyện, sử dụng ngôn ngữ tự nhiên, thân thiện, và tránh quá cứng nhắc.    
    - Sử dụng câu ngắn gọn, tự nhiên , thân thiện gần gũi nhưng không quá sến súa.  
    - Nếu câu hỏi không rõ, hãy hỏi lại thay vì giả định sai.  
    - Đừng lặp lại câu từ cứng nhắc từ câu hỏi.  

    Context:
    {context}
    
    Question: {question}"""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # LLM
    # llm = ChatOpenAI(model_name="gpt-4", temperature=0.6)
    llm = ChatOpenAI(model_name= os.getenv("MODEL_OPENAI_NAME"), temperature=0.6 , streaming=True)

    # Chain
    rag_chain = (
        RunnableMap({"context": RunnablePassthrough(), "question": RunnablePassthrough()})
        | prompt
        | llm
        | StrOutputParser ()
    )
    
    async for chunk in rag_chain.astream({"context": context, "question": user_message}):
        yield chunk  # Trả về từng phần của kết quả