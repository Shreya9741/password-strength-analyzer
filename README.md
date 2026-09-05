# Thiranex Cyber Security Internship
## Password Strength Analyzer

A beginner-friendly full-stack cybersecurity project built with:

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite

### Features

1. Password length and complexity analysis
2. Uppercase/lowercase/number/special-character checks
3. Common-password detection
4. Repeated-character and predictable-sequence checks
5. Score from 0–100
6. Estimated entropy
7. Personalized security suggestions
8. Strong random password generation using Python `secrets`
9. Optional local password-reuse history using SQLite
10. Password history stores SHA-256 hashes instead of plaintext passwords

### Important security note

This is an educational internship project, not a production authentication system.
For real user authentication, use a password-hashing algorithm designed for password storage
such as Argon2id, scrypt, or bcrypt, with appropriate salts and secure session handling.

---

# HOW TO RUN

## Step 1 — Install Python

Install Python 3.11+ from the official Python website.

During Windows installation, IMPORTANT:
tick **Add Python to PATH**.

Check installation:

```bash
python --version
```

If `python` does not work on Windows, try:

```bash
py --version
```

## Step 2 — Open the project

Extract this ZIP.

Open the extracted `Thiranex_Password_Strength_Analyzer` folder in VS Code.

## Step 3 — Open the VS Code terminal

VS Code:
**Terminal → New Terminal**

## Step 4 — Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

If PowerShell blocks activation, use:

```bash
venv\Scripts\activate.bat
```

or run the project with the Python inside the environment.

## Step 5 — Install Flask

```bash
python -m pip install -r requirements.txt
```

Only Flask needs to be installed. SQLite and the other Python modules used here are included with Python.

## Step 6 — Run the project

```bash
python app.py
```

You should see:

```text
Password Strength Analyzer
Open: http://127.0.0.1:5000/
```

Open this in your browser:

http://127.0.0.1:5000/

## Step 7 — Stop the server

In the terminal press:

```text
Ctrl + C
```

---

# PROJECT STRUCTURE

```text
Thiranex_Password_Strength_Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

After the first run, this file is automatically created:

```text
password_history.db
```

Do not manually create it.

---

# HOW TO DEMONSTRATE TO THIRANEX

Try these examples:

Weak:
```text
123456
```

Moderate:
```text
Shreya123
```

Stronger:
```text
Shreya@2026College
```

Generated example:
The **Generate Strong Password** button creates a random password.

Then:
1. Click **Check Reuse**
2. Click **Save to Local History**
3. Click **Check Reuse** again
4. The project detects the password as reused

---

# RESUME DESCRIPTION

**Password Strength Analyzer | Python, Flask, JavaScript, SQLite**

Developed a web-based cybersecurity tool to evaluate password strength using
length, character complexity, common-password detection, repetition and
predictable-sequence analysis. Implemented secure random password generation
using Python `secrets` and a local SQLite password-history feature that stores
hashed values rather than plaintext passwords.

---

# POSSIBLE INTERVIEW QUESTIONS

1. Why did you use Flask?
2. What is password entropy?
3. Why should passwords not be stored as plaintext?
4. What is hashing?
5. Why is SHA-256 not the ideal production password-storage algorithm?
6. What is the difference between hashing and encryption?
7. Why did you use Python `secrets` instead of `random`?
8. What does SQLite do in this project?
9. How does the password reuse check work?
10. How would you improve this project for production?

A strong interview answer for question 7:

> `secrets` is designed for security-sensitive random values, while the
> standard `random` module is intended for general-purpose pseudo-random
> operations and should not be used for security-sensitive password generation.
