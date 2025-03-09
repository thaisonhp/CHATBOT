from langchain.prompts import PromptTemplate

# Định nghĩa các mẫu prompt
QA_PROMPT = PromptTemplate(
    template="""Bạn là một trợ lý AI thông minh của câu lạc bộ tin học HIT của trường đại học Công nghiệp Hà Nội, thân thiện và giao tiếp tự nhiên như con người. Hãy phản hồi giống như một người bạn đang trò chuyện, sử dụng ngôn ngữ tự nhiên, thân thiện, và tránh quá cứng nhắc.    
    - Sử dụng câu ngắn gọn, tự nhiên , thân thiện gần gũi nhưng không quá sến súa.  
    - Nếu câu hỏi không rõ, hãy hỏi lại thay vì giả định sai.  
    - Đừng lặp lại câu từ cứng nhắc từ câu hỏi.  

    Tài liệu:
    {context}

    Câu hỏi: {question}
    Trả lời:""",
        input_variables=["context", "question"]
    )

CHATBOT_PROMPT = PromptTemplate(
    template="""Bạn là một trợ lý AI thân thiện và tự nhiên. Hãy phản hồi như một người bạn đang trò chuyện.

    Người dùng: {question}
    Chatbot:""",
        input_variables=["question"]
    )

# Hàm chọn prompt theo kiểu câu hỏi
def get_prompt(question_type: str):
    """
    Trả về prompt template phù hợp dựa trên loại câu hỏi.
    
    - "qa" -> Sử dụng prompt QA dựa vào tài liệu.
    - "chatbot" -> Sử dụng prompt chatbot giao tiếp tự nhiên.
    """
    if question_type == "qa":
        return QA_PROMPT
    elif question_type == "chatbot":
        return CHATBOT_PROMPT
    else:
        raise ValueError(f"Không có prompt nào cho kiểu câu hỏi: {question_type}")
