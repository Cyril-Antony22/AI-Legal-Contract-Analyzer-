// Module 7 - AI Legal Chat: sends the user's question to the Flask backend
// and prints the AI's answer into the chat box, without reloading the page.
async function askQuestion(contractId) {
    const input = document.getElementById("questionInput");
    const question = input.value.trim();
    if (!question) return;

    const chatBox = document.getElementById("chatBox");

    const placeholder = chatBox.querySelector("p.text-muted");
    if (placeholder) placeholder.remove();

    chatBox.innerHTML += `
        <div class="chat-msg user">
            <span class="who">You asked</span>${question}
        </div>`;
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    const response = await fetch(`/chat/${contractId}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
    });
    const data = await response.json();

    chatBox.innerHTML += `
        <div class="chat-msg ai">
            <span class="who">AI answered</span>${data.answer || data.error}
        </div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Part 2 bridge - "Share Contract Report" button on the results page.
async function shareReport(contractId) {
    const email = document.getElementById("recipientEmail").value.trim();
    const status = document.getElementById("shareStatus");
    if (!email) {
        status.innerHTML = `<span style="color: var(--redline);">Please enter an email.</span>`;
        return;
    }

    status.innerHTML = "Sending...";
    const response = await fetch(`/share/${contractId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipient_email: email })
    });
    const data = await response.json();

    status.innerHTML = data.ok
        ? `<span style="color: #4a8073;">Sent! Make.com will email the report shortly.</span>`
        : `<span style="color: var(--redline);">Failed: ${data.error}</span>`;
}