const passwordInput = document.getElementById("password");
const rating = document.getElementById("rating");
const score = document.getElementById("score");
const meterFill = document.getElementById("meterFill");
const checksBox = document.getElementById("checks");
const suggestionsBox = document.getElementById("suggestions");
const entropy = document.getElementById("entropy");
const statusBox = document.getElementById("status");

const labels = {
    length: "At least 12 characters",
    uppercase: "Uppercase letter",
    lowercase: "Lowercase letter",
    number: "Number",
    special: "Special character",
    common: "Not a common password",
    repetition: "No repeated characters",
    sequence: "No predictable sequence"
};

function showStatus(message) {
    statusBox.textContent = message;
}

function render(result) {
    rating.textContent = result.rating;
    score.textContent = `${result.score}/100`;
    meterFill.style.width = `${result.score}%`;
    entropy.textContent = `${result.entropy} bits`;

    checksBox.innerHTML = Object.entries(result.checks).map(([key, passed]) => `
        <div class="check">
            <span>${labels[key]}</span>
            <span class="${passed ? "good" : "bad"}">${passed ? "✓ Pass" : "✗ Improve"}</span>
        </div>
    `).join("");

    suggestionsBox.innerHTML = result.suggestions
        .map(item => `<li>${item}</li>`)
        .join("");
}

async function analyze() {
    const password = passwordInput.value;

    if (!password) {
        render({
            rating: "Enter a password",
            score: 0,
            entropy: 0,
            checks: Object.fromEntries(Object.keys(labels).map(k => [k, false])),
            suggestions: ["Enter a password to see personalized recommendations."]
        });
        return;
    }

    const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({password})
    });

    const result = await response.json();
    render(result);
}

passwordInput.addEventListener("input", analyze);

document.getElementById("toggleBtn").addEventListener("click", () => {
    const btn = document.getElementById("toggleBtn");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        btn.textContent = "Hide";
    } else {
        passwordInput.type = "password";
        btn.textContent = "Show";
    }
});

document.getElementById("generateBtn").addEventListener("click", async () => {
    const response = await fetch("/api/generate", {method: "POST"});
    const data = await response.json();
    passwordInput.value = data.password;
    passwordInput.type = "text";
    document.getElementById("toggleBtn").textContent = "Hide";
    render(data.analysis);
    showStatus("A strong random password was generated. Store it safely in a password manager.");
});

document.getElementById("historyBtn").addEventListener("click", async () => {
    if (!passwordInput.value) {
        showStatus("Enter a password first.");
        return;
    }

    const response = await fetch("/api/history/check", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({password: passwordInput.value})
    });

    const data = await response.json();
    showStatus(data.reused
        ? "⚠ This password already exists in your local password history. Avoid reusing it."
        : "✓ This password was not found in your local password history.");
});

document.getElementById("saveBtn").addEventListener("click", async () => {
    if (!passwordInput.value) {
        showStatus("Enter a password first.");
        return;
    }

    const response = await fetch("/api/history/save", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({password: passwordInput.value})
    });

    const data = await response.json();
    showStatus(data.saved
        ? "✓ Password hash saved to local history. The plaintext password is not stored."
        : "This password is already in local history.");
});

analyze();
