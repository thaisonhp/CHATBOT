from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from chromadb import PersistentClient

def process_query(user_message: str):
    # Kết nối ChromaDB
    client = PersistentClient(path="./chroma_db")
    vectorstore = Chroma(client=client, collection_name="langchain", embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # Truy vấn 5 tài liệu liên quan nhất

    # Lấy tài liệu từ ChromaDB
    docs = retriever.invoke(user_message)

    # Định dạng tài liệu thành một chuỗi context
    context = "\n\n".join(doc.page_content for doc in docs)

    # Prompt Template
    template = """You are an AI assistant. Answer the question based on the given context.
    
    Context:
    {context}
    
    Question: {question}"""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Chain
    rag_chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    # Nhập context và câu hỏi vào chain
    answer = rag_chain.invoke({"context": context, "question": user_message})
    return answer

answer = process_query("xin chào")
print(answer.content)