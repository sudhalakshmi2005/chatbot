function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");

    if (userInput.trim() === "") return;

    let userMessage = `<div class="message user">${userInput}</div>`;
    chatBox.innerHTML += userMessage;
    document.getElementById("user-input").value = "";

    let botMessageDiv = document.createElement("div");
    botMessageDiv.classList.add("message", "bot");
    chatBox.appendChild(botMessageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: userInput }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        function readStream() {
            reader.read().then(({ done, value }) => {
                if (done) return;
                botMessageDiv.innerHTML += decoder.decode(value);
                chatBox.scrollTop = chatBox.scrollHeight;
                readStream();
            });
        }
        readStream();
    })
    .catch(error => {
        botMessageDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    });
}

function uploadImage() {
    let imageInput = document.getElementById("image-input");
    let file = imageInput.files[0];

    if (!file) {
        alert("Please select an image to upload.");
        return;
    }

    let formData = new FormData();
    formData.append("image", file);

    fetch("/chat", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.image_url) {
            let chatBox = document.getElementById("chat-box");
            let imageMessage = `<div class="message user"><img src="${data.image_url}" width="150"/></div>`;
            chatBox.innerHTML += imageMessage;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    })
    .catch(error => {
        console.error("Image upload error:", error);
    });
}
