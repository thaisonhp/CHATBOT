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
            setTimeout(() => {
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 50);
            
        }

    } catch (error) {
        chatBox.innerHTML += `<div class="chat-message bot">Lỗi kết nối!</div>`;
    }
}

async function uploadFile() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "application/pdf";

    input.onchange = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:8001/upload-pdf/", {
                method: "POST",
                body: formData
            });

            const result = await response.json();
            console.log("📂 Kết quả trả về:", result);

            if (response.ok) {
                alert("📂 Tải lên thành công!");
            } else {
                alert("❌ Lỗi tải lên: " + result.detail);
            }
        } catch (error) {
            console.error("❌ Lỗi:", error);
            alert("❌ Lỗi kết nối đến server!");
        }
    };

    input.click();
}


