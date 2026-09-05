# Password Strength Analyzer — Mini Project Report

## 1. Objective
Develop a tool that evaluates the strength of user-entered passwords and provides
security recommendations.

## 2. Technologies
Python, Flask, HTML, CSS, JavaScript and SQLite.

## 3. Main Features
- Password length check
- Complexity check
- Common-password detection
- Repetition and sequence detection
- Strength score
- Entropy estimate
- Strong password generation
- Local password reuse history

## 4. Working
The browser sends the entered password to the Flask backend through an API endpoint.
The backend evaluates the password against several security rules and returns a
score, rating, checks and recommendations. The generated password uses Python's
`secrets` module.

For the optional reuse feature, the application hashes the password with SHA-256
and compares the hash against locally stored password-history hashes. Plaintext
passwords are not stored.

## 5. Security Limitation
SHA-256 is used here for demonstrating hashing and local comparison. A production
authentication system should use a password-specific algorithm such as Argon2id,
scrypt or bcrypt and should follow current password-storage best practices.

## 6. Expected Outcome
The project demonstrates practical knowledge of password security, hashing,
secure random generation, backend APIs, frontend interaction and database basics.
