async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const userMessage = inputField.value.trim();
    
    if (userMessage === "") return;

    // Thêm tin nhắn người dùng vào giao diện
    chatBox.innerHTML += `<div class="chat-message user">${userMessage}</div>`;
    inputField.value = ""; 
    chatBox.scrollTop = chatBox.scrollHeight; 

    try {
        const response = await fetch("http://0.0.0.0:8001/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: userMessage })
        });

        if (!response.body) throw new Error("Phản hồi không có nội dung");

        // Tạo phần tử mới cho tin nhắn bot
        const botMessageElem = document.createElement("div");
        botMessageElem.classList.add("chat-message", "bot");
        chatBox.appendChild(botMessageElem);

        // Đọc dữ liệu streaming
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let botReply = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            botReply += decoder.decode(value, { stream: true });

            // Cập nhật nội dung tin nhắn bot theo thời gian thực
            botMessageElem.innerHTML = botReply;
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    } catch (error) {
        chatBox.innerHTML += `<div class="chat-message bot">Lỗi kết nối!</div>`;
    }
}
