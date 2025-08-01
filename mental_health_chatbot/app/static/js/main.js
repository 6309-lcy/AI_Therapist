function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput, user_id: 'default_user' })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
        playVoiceOutput(data.audio_id);
        console.log('Sentiment:', data.sentiment, 'Depression Level:', data.depression_level);
        document.getElementById('user-input').value = '';
    })
    .catch(error => console.error('Error:', error));
}

function requestStaff() {
    fetch('/staff_intervention/default_user')
    .then(response => response.json())
    .then(data => {
        alert('Staff notified. Conversation history: ' + JSON.stringify(data.conversation));
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});