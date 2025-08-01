function playVoiceOutput(text) {
    // Placeholder for ElevenLabs audio playback
    // Actual implementation requires ElevenLabs WebSocket or audio streaming
    fetch('/generate_audio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.blob())
    .then(blob => {
        const audio = new Audio(URL.createObjectURL(blob));
        audio.play();
    })
    .catch(error => console.error('Error playing audio:', error));
}