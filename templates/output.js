// Example: Load AI chatbot output (mockup)
document.addEventListener('DOMContentLoaded', function() {
    const outputDiv = document.querySelector('.output');
    outputDiv.textContent = 'AI chatbot output loaded...'; // Placeholder text
    // Here you would fetch and display real AI output
});
function goHome() {
    // Navigate to the homepage
    window.location.href = '/'; // Assuming '/' is your homepage
}

function startNewChat() {
    // For demonstration purposes, this could reload the page to simulate starting a new chat
    // In a real application, you would likely reset the chat interface or navigate to a chat page
    window.location.reload();
}

function logout() {
    // This function needs to interact with the server to log a user out
    // For demonstration, we'll just navigate to a login page
    window.location.href = '/login'; // Adjust this path to your actual login page
}
function logout() {
    fetch('/logout', {
        method: 'POST', // Or the appropriate method for your backend
        // Additional headers or credentials as needed
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/login';
        } else {
            console.error('Logout failed');
        }
    })
    
    .catch(error => console.error('Error:', error));
}
function downloadOutput() {
    // Assuming your output is plain text and is inside .output div
    const outputText = document.querySelector('.output').textContent; // Get the text content
    const blob = new Blob([outputText], { type: 'text/plain' });
    const href = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = href;
    link.download = "output.txt"; // Filename for download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
function shareOutput() {
    const outputText = document.querySelector('.output').textContent; // Get the text content
    if (navigator.share) {
        navigator.share({
            title: 'Check out this content!',
            text: outputText,
            url: document.location.href
        }).then(() => {
            console.log('Content shared successfully');
        }).catch((error) => {
            console.log('Error sharing content', error);
        });
    } else {
        alert("Your browser doesn't support the Share API.");
    }
}
