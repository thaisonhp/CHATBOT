from langchain.tools import Tool
from utils.pre_retrival import vector_search
from langchain_openai import ChatOpenAI

# Khởi tạo mô hình GPT-4 với nhiệt độ thấp để có đầu ra ổn định
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

def query_routing(query: str):
    """Sử dụng LLM để phân loại truy vấn vào các nhóm phù hợp"""
    categories = [
        "vector_search", "web_search", "math_solver", "sql_query",
        "translation", "text_summarization", "document_reader",
        "image_recognition"
    ]
    
    prompt = (
        f"Hãy phân loại câu hỏi này vào một trong các danh mục sau: {categories}. Hãy ưu tiên vector_search nếu không có trong database thì hẵng web_search"
        f"Chỉ trả về tên danh mục, không có văn bản khác.\n\nCâu hỏi: {query}"
    )

    result = llm.invoke(prompt)
    print(result.content)
    if result in categories:
        return result
    return "vector_search"  # Mặc định nếu mô hình không phân loại đúng

# Định nghĩa các công cụ
tools = {
    "vector_search": vector_search,
    # "web_search": web_search,
    # "math_solver": math_solver,
    # "sql_query": sql_query,
    # "translation": translation,
    # "text_summarization": text_summarization,
    # "document_reader": document_reader,
    # "image_recognition": image_recognition,
}

