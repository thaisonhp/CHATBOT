import chainlit as cl
import requests

API_BASE_URL = "http://localhost:8001"  # Cập nhật URL nếu FastAPI chạy ở nơi khác

@cl.on_message
async def handle_message(message: cl.Message):
    response = requests.post(f"{API_BASE_URL}/chat", json={"text": message.content})
    if response.status_code == 200:
        reply = response.json()["response"]
    else:
        reply = "Lỗi khi gọi API."

    await cl.Message(content=reply).send()

# @cl
# async def handle_file(file: cl.File):
#     files = {"file": (file.name, file.content, file.mime)}
#     response = requests.post(f"{API_BASE_URL}/upload-pdf/", files=files)
#     if response.status_code == 200:
#         reply = "Tải lên và xử lý file thành công!"
#     else:
#         reply = f"Lỗi: {response.json().get('detail', 'Không xác định')}"

#     await cl.Message(content=reply).send()
