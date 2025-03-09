from langchain.tools import Tool

def query_routing(query: str):
    """Hàm định tuyến truy vấn dựa trên nội dung"""
    if "solve" in query or "calculate" in query or any(c.isdigit() for c in query):
        return "math_solver"
    elif "latest" in query or "news" in query:
        return "web_search"
    elif "database" in query or "SQL" in query:
        return "sql_query"
    elif "translate" in query:
        return "translation"
    elif "summary" in query:
        return "text_summarization"
    elif "document" in query or "pdf" in query:
        return "document_reader"
    elif "image" in query:
        return "image_recognition"
    else:
        return "vector_search"  # Mặc định tìm trong database

# Định nghĩa các công cụ
tools = {
    "vector_search": vector_search,
    "web_search": web_search,
    "math_solver": math_solver,
    "sql_query": sql_query,
    "translation": translation,
    "text_summarization": text_summarization,
    "document_reader": document_reader,
    "image_recognition": image_recognition,
}

# Gọi đúng hàm theo loại truy vấn
query = "Translate 'hello' to French"
selected_tool = query_routing(query)
response = tools[selected_tool](query)

print(f"Using {selected_tool}: {response}")
