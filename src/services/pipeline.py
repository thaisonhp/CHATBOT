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
import os
from utils.classification_query import detect_question_type
from models.prompt_template import get_prompt
from services.pre_retrival import query_routing , tools
load_dotenv()

# 4. Pipeline RAG hoàn chỉnh
async def rag_pipeline(user_message: str):
    
    selected_tool = query_routing(user_message)
    context = tools[selected_tool](user_message)

    type_querry = detect_question_type(user_message)
    prompt = get_prompt(type_querry)

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
