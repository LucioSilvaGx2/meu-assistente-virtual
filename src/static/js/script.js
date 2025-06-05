document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Função para adicionar uma mensagem ao chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        messageDiv.appendChild(paragraph);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Função para enviar mensagem para a API
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        addMessage(message, 'client');
        userInput.value = '';

        if (message.toLowerCase() === 'sair') {
            addMessage('Obrigado por usar o Assistente Virtual da LLMS. Até a próxima!', 'assistant');
            userInput.disabled = true;
            sendButton.disabled = true;
            return;
        }

        // Adiciona "Digitando..." como placeholder da resposta
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'assistant');
        const typingText = document.createElement('p');
        typingText.textContent = 'Digitando...';
        typingDiv.appendChild(typingText);
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const response = await fetch('/api/assistenteDigital', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mensagem: message }) // Certo: 'mensagem'
            });

            if (!response.ok) {
                throw new Error(`Erro HTTP! Status: ${response.status}`);
            }

            const data = await response.json();

            // Espera artificial (opcional) para parecer mais natural
            await new Promise(resolve => setTimeout(resolve, 500));

            typingText.textContent = data.resposta || 'Desculpe, não consegui entender sua pergunta.';

        } catch (error) {
            console.error('Erro ao comunicar com a API:', error);
            typingText.textContent = 'Ops! Houve um problema ao conectar com o assistente. Tente novamente mais tarde.';
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
