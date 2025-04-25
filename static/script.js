document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // Generate a unique session ID for this chat session
    const sessionId = 'session_' + Date.now();
    
    // Function to add a message to the chat
    function addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
        
        const avatar = document.createElement('div');
        avatar.className = isUser ? 'avatar user-avatar' : 'avatar bot-avatar';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Instead of using textContent, use innerHTML with line breaks converted to <br> tags
        // This preserves the line breaks from the API response
        messageContent.innerHTML = message.replace(/\n/g, '<br>');
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to handle sending a message
    function sendMessage() {
        const message = userInput.value.trim();
        
        if (message === '') {
            return;
        }
        
        // Add the user's message to the chat
        addMessage(message, true);
        
        // Clear the input field
        userInput.value = '';
        
        // Show loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message';
        loadingDiv.id = 'loading-message';
        
        const loadingAvatar = document.createElement('div');
        loadingAvatar.className = 'avatar bot-avatar';
        
        const loadingContent = document.createElement('div');
        loadingContent.className = 'message-content';
        loadingContent.textContent = 'Pensando...';
        
        loadingDiv.appendChild(loadingAvatar);
        loadingDiv.appendChild(loadingContent);
        
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Send the message to the server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove the loading message
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                chatMessages.removeChild(loadingMessage);
            }
            
            // Add the bot's response to the chat
            if (data.response) {
                addMessage(data.response, false);
            } else if (data.error) {
                addMessage('Desculpe, tive um problema ao processar sua mensagem. Tente novamente.', false);
                console.error('Error:', data.error);
            }
        })
        .catch(error => {
            // Remove the loading message
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                chatMessages.removeChild(loadingMessage);
            }
            
            // Add an error message to the chat
            addMessage('Desculpe, tive um problema de conexão. Verifique sua internet e tente novamente.', false);
            console.error('Error:', error);
        });
    }
    
    // Send message when the send button is clicked
    sendButton.addEventListener('click', sendMessage);
    
    // Send message when Enter key is pressed
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});