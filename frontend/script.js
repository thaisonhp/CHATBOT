async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const userMessage = inputField.value.trim();
    
    if (userMessage === "") return;

    // Thêm tin nhắn người dùng vào giao diện
    chatBox.innerHTML += `<div class="chat-message user">${userMessage}</div>`;
    inputField.value = ""; 
    chatBox.scrollTop = chatBox.scrollHeight; 

    // Gửi tin nhắn đến API FastAPI
    try {
        const response = await fetch("http://0.0.0.0:8001/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: userMessage })
        });

        const data = await response.json();
        const botReply = data.response || "Xin lỗi, tôi chưa hiểu.";

        // Thêm phản hồi của chatbot
        chatBox.innerHTML += `<div class="chat-message bot">${botReply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight; 
    } catch (error) {
        chatBox.innerHTML += `<div class="chat-message bot">Lỗi kết nối!</div>`;
    }
}
