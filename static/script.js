document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // Gera um ID para a sessão atual
    const sessionId = 'session_' + Date.now();
    
    // Funcão para adicionar mensagem ao chat
    function addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
        
        const avatar = document.createElement('div');
        avatar.className = isUser ? 'avatar user-avatar' : 'avatar bot-avatar';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        messageContent.innerHTML = message.replace(/\n/g, '<br>');
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Função para o envio da mensagem
    function sendMessage() {
        const message = userInput.value.trim();
        
        if (message === '') {
            return;
        }
        
        // Adiciona a mensagem do usuário no chat
        addMessage(message, true);
        
        // Limpa o campo de texto
        userInput.value = '';
        
        // indicador de loading do modelo
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
        
        // Envia a mensagem ao servidor
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
            // Remove o indicador de loading
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                chatMessages.removeChild(loadingMessage);
            }
            
            // Adiciona a resposta do modelo no chat
            if (data.response) {
                addMessage(data.response, false);
            } else if (data.error) {
                addMessage('Desculpe, tive um problema ao processar sua mensagem. Tente novamente.', false);
                console.error('Error:', data.error);
            }
        })
        .catch(error => {
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                chatMessages.removeChild(loadingMessage);
            }
            
            addMessage('Desculpe, tive um problema de conexão.', false);
            console.error('Error:', error);
        });
    }
    
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    function ajustarJanelaComTeclado() {
        const chatContainer = document.querySelector('.chat-container');
        window.addEventListener('resize', function () {
            if (window.innerHeight < 500) { 
                chatContainer.style.bottom = '50%'; 
            } else {
                chatContainer.style.bottom = '0';
            }
        });
    }
    ajustarJanelaComTeclado();
});