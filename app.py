from flask import Flask, render_template, request, jsonify
import hashlib
import math
import re
import secrets
import sqlite3
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "password_history.db"

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678", "123456789",
    "qwerty", "qwerty123", "admin", "admin123", "welcome",
    "letmein", "iloveyou", "abc123", "monkey", "dragon",
    "football", "login", "user", "pass", "test", "india123",
    "college123", "student123", "computer123", "cyber123"
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS password_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn

def hash_password(password):
    # SHA-256 is used here only to compare locally stored password history.
    # Real production authentication should use Argon2/bcrypt/scrypt with salts.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def estimate_entropy(password):
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[^A-Za-z0-9]", password):
        pool += 32
    if pool == 0 or not password:
        return 0
    return round(len(password) * math.log2(pool), 1)

def analyze_password(password):
    length = len(password)
    checks = {
        "length": length >= 12,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[^A-Za-z0-9]", password)),
        "common": password.lower() not in COMMON_PASSWORDS,
        "repetition": not bool(re.search(r"(.)\1{2,}", password)),
        "sequence": not bool(re.search(
            r"(0123|1234|2345|3456|4567|5678|6789|abcd|bcde|cdef|qwer)",
            password.lower()
        )),
    }

    score = 0
    if length >= 8: score += 15
    if length >= 12: score += 15
    if length >= 16: score += 10
    if checks["uppercase"]: score += 10
    if checks["lowercase"]: score += 10
    if checks["number"]: score += 10
    if checks["special"]: score += 15
    if checks["common"]: score += 10
    if checks["repetition"]: score += 3
    if checks["sequence"]: score += 2

    entropy = estimate_entropy(password)

    if not password:
        rating = "Enter a password"
        level = "empty"
    elif score < 40:
        rating = "Weak"
        level = "weak"
    elif score < 65:
        rating = "Moderate"
        level = "moderate"
    elif score < 85:
        rating = "Strong"
        level = "strong"
    else:
        rating = "Very Strong"
        level = "very-strong"

    suggestions = []
    if length < 12:
        suggestions.append("Use at least 12 characters; 16+ is even better.")
    if not checks["uppercase"]:
        suggestions.append("Add uppercase letters.")
    if not checks["lowercase"]:
        suggestions.append("Add lowercase letters.")
    if not checks["number"]:
        suggestions.append("Add numbers.")
    if not checks["special"]:
        suggestions.append("Add special characters such as !, @, # or $.")
    if not checks["common"]:
        suggestions.append("Avoid common passwords and predictable words.")
    if not checks["repetition"]:
        suggestions.append("Avoid repeating the same character three or more times.")
    if not checks["sequence"]:
        suggestions.append("Avoid predictable sequences such as 1234, abcd or qwer.")

    if not suggestions and password:
        suggestions.append("Good password structure. Keep it unique and never reuse it.")

    return {
        "score": min(score, 100),
        "rating": rating,
        "level": level,
        "entropy": entropy,
        "checks": checks,
        "suggestions": suggestions,
    }

def generate_password(length=18):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*_-+="
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        result = analyze_password(password)
        if result["score"] >= 85:
            return password

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def api_analyze():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if not isinstance(password, str):
        return jsonify({"error": "Invalid password value."}), 400
    return jsonify(analyze_password(password))

@app.post("/api/generate")
def api_generate():
    password = generate_password(18)
    return jsonify({
        "password": password,
        "analysis": analyze_password(password)
    })

@app.post("/api/history/check")
def check_history():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if not isinstance(password, str) or not password:
        return jsonify({"error": "Enter a password first."}), 400

    password_hash = hash_password(password)
    conn = get_db()
    row = conn.execute(
        "SELECT 1 FROM password_history WHERE password_hash = ?",
        (password_hash,)
    ).fetchone()
    conn.close()

    return jsonify({"reused": row is not None})

@app.post("/api/history/save")
def save_history():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if not isinstance(password, str) or not password:
        return jsonify({"error": "Enter a password first."}), 400

    password_hash = hash_password(password)
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO password_history(password_hash) VALUES (?)",
            (password_hash,)
        )
        conn.commit()
        saved = True
    except sqlite3.IntegrityError:
        saved = False
    finally:
        conn.close()

    return jsonify({"saved": saved})

if __name__ == "__main__":
    get_db().close()
    print("\nPassword Strength Analyzer")
    print("Open: http://127.0.0.1:5000\n")
    app.run(debug=True)
