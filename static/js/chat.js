function handleMessageInput(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function addMessageToChat(markdownText, isUserMessage = false) {
    // Convert markdown to HTML
    const htmlContent = marked.parse(markdownText);

    // Create a new message element
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerHTML = htmlContent;

    if (isUserMessage) {
        messageElement.classList.add('user-message');
    } else {
        messageElement.classList.add('bot-message');
    }

    // Append the message to the chat window
    const chatWindow = document.getElementById('chat-window');
    chatWindow.appendChild(messageElement);

    // Scroll to the bottom of the chat window
    chatWindow.scrollTop = chatWindow.scrollHeight;
}


function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value;

    if (message.trim() !== '') {
        // Display user message
        addMessageToChat(message, true);

        // Clear input
        input.value = '';

        // Send message to LLM API
        fetch('/api/chat/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
            .then(response => response.json())
            .then(data => {
                // Display LLM response
                addMessageToChat(data.reply, false)
            });
    }
}