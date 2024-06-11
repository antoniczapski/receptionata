
let conversationHistory = [];

fetch('static/instructions.txt')
  .then(response => response.text())
  .then(data => {
    conversationHistory = [{sender: 'system', message: data}];
    // document.getElementById('agent-instructions-textarea').value = data;
  });


async function sendMessage() {
    var prompt = document.getElementById('prompt-textarea').value;
    document.getElementById('prompt-textarea').value = '';
    displayMessage('user', prompt);

    conversationHistory.push({ sender: 'user', message: prompt });

    try {
        const result = await generateChatbotResponse(conversationHistory);
        const [response, backend_response] = result;
        displayMessage('assistant', response)
        conversationHistory.push({ sender: 'assistant', message: response });

        // Update textareas and check their content to adjust dropdowns
        const textAreas = [
            document.getElementById('agent-instructions-textarea'),
            document.getElementById('agent-instructions-textarea-2'),
            document.getElementById('agent-instructions-textarea-3')
        ];

        backend_response.forEach((content, index) => {
            const textarea = textAreas[index];
            const dropdown = textarea.parentNode.parentNode;
            const button = dropdown.querySelector('.dropdown-btn');
            const indicator = button.querySelector('.indicator');
            console.log(content);
            textarea.value = content;

            if (content.trim() === '') {
                button.disabled = true;  // Disable the button if no content
                indicator.textContent = '-';  // Set indicator to '-' for empty
                textarea.parentNode.style.maxHeight = null;  // Close dropdown if it was open
            } else {
                button.disabled = false;  // Enable button if there's content
                indicator.textContent = '+';  // Set indicator to '+' to show it's openable
            }
        });

    } catch (error) {
        console.error('Error:', error);
    }
}


function displayMessage(sender, message) {
    if (sender === 'system') {
        return;
    }
    var chatDiv = document.getElementById('chat');
    var messageDiv = document.createElement('div');
    var imageDiv = document.createElement('img');
    var textDiv = document.createElement('div');
    
    var senderTextNode = document.createElement('div');
    var messageTextNode = document.createElement('div');

    senderTextNode.className = 'chat-sender';
    messageTextNode.className = sender === 'user' ? 'chat-message-text-user' : 'chat-message-text-bot';

    senderTextNode.textContent = sender;
    if (sender === 'user') {
        messageTextNode.textContent = message;
    }
    else {
        var formattedMessage = message.replace(/\n/g, '<br>');
        formattedMessage = formattedMessage.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        messageTextNode.innerHTML = formattedMessage;
    }

    textDiv.appendChild(senderTextNode);
    textDiv.appendChild(messageTextNode);

    textDiv.className = 'chat-text';

    let userImg = document.body.getAttribute('data-user-img');
    let botImg = document.body.getAttribute('data-bot-img');

    imageDiv.src = sender === 'user' ? userImg : botImg;
    imageDiv.className = 'chat-image';

    messageDiv.className = 'chat-message';
    messageDiv.appendChild(imageDiv);
    messageDiv.appendChild(textDiv);

    chatDiv.appendChild(messageDiv);

    messageDiv.scrollIntoView({ behavior: 'smooth' });
}

async function generateChatbotResponse(conversationHistory) {
    const response = await fetch('/run_script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(conversationHistory)
    });

    if (response.ok) {
        const result = await response.json();
        return result;
    } else {
        console.error('Error calling Python script:', response.status, response.statusText);
    }
}

var textarea = document.getElementById('prompt-textarea');
textarea.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});


document.addEventListener('DOMContentLoaded', function() {
    var dropdowns = document.querySelectorAll('.dropdown-btn');
    dropdowns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var dropdownContent = this.nextElementSibling;
            var indicator = this.querySelector('.indicator'); // Get the indicator span

            // Check if the clicked dropdown is already open
            if (dropdownContent.style.maxHeight && dropdownContent.style.maxHeight !== "0px") {
                // Close the dropdown
                dropdownContent.style.maxHeight = null;
                indicator.textContent = '+'; // Change indicator to '+'
            } else {
                // Close all other dropdowns
                document.querySelectorAll('.dropdown-content').forEach(function(otherContent) {
                    if (otherContent.style.maxHeight && otherContent.style.maxHeight !== "0px") {
                        otherContent.style.maxHeight = null;
                        otherContent.previousElementSibling.querySelector('.indicator').textContent = '+'; // Reset other indicators
                    }
                });

                // Open the clicked dropdown and adjust to content size
                dropdownContent.style.maxHeight = dropdownContent.scrollHeight + "px";
                indicator.textContent = '-'; // Change indicator to '-'
            }
        });
    });
});
