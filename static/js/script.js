const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

function appendMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('content');
    contentDiv.innerText = text;
    
    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('typing-indicator');
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `;
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return typingDiv;
}

function removeTypingIndicator(indicator) {
    if (indicator) {
        indicator.remove();
    }
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (text === "") return;

    appendMessage(text, true);
    userInput.value = '';

    const typingIndicator = showTypingIndicator();

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        
        // Simulate a slight delay for realism if the response is too fast
        setTimeout(() => {
            removeTypingIndicator(typingIndicator);
            appendMessage(data.answer, false);
            // Play sound (optional, simple beep)
            // const audio = new Audio('path/to/sound.mp3');
            // audio.play();
        }, 600); 

    } catch (error) {
        removeTypingIndicator(typingIndicator);
        appendMessage("Sorry, something went wrong. Please check your connection.", false);
        console.error('Error:', error);
    }
}

userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
