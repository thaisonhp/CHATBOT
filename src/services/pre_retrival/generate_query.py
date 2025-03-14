from langchain.prompts import ChatPromptTemplate

# RAG-Fusion: Related
template = """Bạn là một trợ lý hữu ích giúp tạo ra nhiều truy vấn tìm kiếm dựa trên một câu hỏi đầu vào.  
Hãy tạo ra nhiều truy vấn tìm kiếm liên quan đến: {question}  
Trả lời bằng tiếng Việt.  
Kết quả (4 truy vấn):"""

prompt_rag_fusion = ChatPromptTemplate.from_template(template)

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os 

generate_queries = (
    prompt_rag_fusion 
    | ChatOpenAI(name=os.getenv("MODEL_OPENAI_NAME") ,temperature=0)
    | StrOutputParser() 
    | (lambda x: x.split("\n"))
)

