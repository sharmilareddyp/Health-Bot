document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Function to add message to chat interface
    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.innerText = message;
        chatMessages.appendChild(messageElement);
    }

    // Function to handle sending message to chatbot
    function sendMessage() {
        const message = userInput.value.trim();
        if (message !== '') {
            addMessage(message, 'user');
            userInput.value = ''; // Clear input field

            // Send message to Flask backend
            fetch('/api/chat', {
                method: 'POST',
                body: JSON.stringify({ message }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                const botResponse = data.message;
                addMessage(botResponse, 'bot');
            })
            .catch(error => console.error('Error:', error));
        }
    }

    // Event listener for send button
    sendBtn.addEventListener('click', sendMessage);

    // Event listener for pressing Enter key
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
