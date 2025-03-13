from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(model_name= os.getenv("MODEL_OPENAI_NAME"), temperature=0.6 , streaming=True)

def expand_query(query):
    prompt = f"Rewrite the query to be more detailed and specific: {query}"
    return llm.invoke(prompt)

expand_query("How does RAG work?")
# Output: "Explain in detail how Retrieval-Augmented Generation (RAG) works, including its retrieval process and generation step."
