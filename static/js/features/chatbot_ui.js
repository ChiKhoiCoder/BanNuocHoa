// Chatbot UI Feature
document.addEventListener('DOMContentLoaded', function() {
    const chatbotBtn = document.querySelector('[data-chatbot-toggle]');
    const chatWindow = document.querySelector('[data-chatbot-window]');
    
    if (chatbotBtn && chatWindow) {
        chatbotBtn.addEventListener('click', () => {
            chatWindow.classList.toggle('open');
        });
    }
});
