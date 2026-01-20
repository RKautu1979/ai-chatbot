document.addEventListener("DOMContentLoaded", () => {

    const chatBtn = document.getElementById("chatbot-btn");
    const chatWindow = document.getElementById("chatbot-window");
    const closeChat = document.getElementById("close-chat");
    const newChat = document.getElementById("new-chat");
    const messages = document.getElementById("chatbot-messages");
    const input = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");

    let isOpen = false;
    let greeted = false; // Prevent double greeting

    // Toggle Chat
    chatBtn.addEventListener("click", () => {
        isOpen = !isOpen;
        chatWindow.classList.toggle("open", isOpen);

        // Auto greet once per open
        if (isOpen && !greeted) {
            setTimeout(() => {
                addMessage("Hello, how can I help?", "bot");
            }, 350);
            greeted = true;
        }
    });

    // Close chat
    closeChat.addEventListener("click", () => {
        isOpen = false;
        chatWindow.classList.remove("open");
    });

    // New chat
    newChat.addEventListener("click", () => {
        messages.innerHTML = "";
        greeted = false; // allow greeting on next open
    });

    // Sending
    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", e => {
        if (e.key === "Enter") sendMessage();
    });

    function addMessage(text, sender) {
        const div = document.createElement("div");
        div.classList.add("message", sender);
        div.innerText = text;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    function showTyping() {
        const div = document.createElement("div");
        div.classList.add("message", "bot", "typing");
        div.innerText = "Typing...";
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
        return div;
    }

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        addMessage(text, "user");
        input.value = "";

        const typingDiv = showTyping();

        try {
            const res = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            const data = await res.json();

            typingDiv.remove();
            addMessage(data.reply, "bot");

        } catch (e) {
            typingDiv.remove();
            addMessage("Error: Cannot connect to server.", "bot");
        }
    }
});