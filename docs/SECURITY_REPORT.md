# Security Report

## Project Name

Secure Login System with Vulnerability Fixes

---

## 1. Introduction

Authentication is one of the most important parts of any web application. A login system is used to verify users and allow only authorized users to access protected pages.

A weak login system can create serious security problems such as password leakage, SQL injection, brute-force attacks, and unauthorized access. This project focuses on building a basic login system and improving it using secure coding practices.

This project is developed using Python Flask and SQLite. It demonstrates how common authentication vulnerabilities can be identified and fixed in a beginner-friendly web application.

---

## 2. Objective

The main objective of this project is to build a secure login system and understand basic web application security concepts.

The objectives of this project are:

- To create a user registration and login system.
- To store passwords securely using hashing.
- To prevent SQL injection using parameterized queries.
- To reduce brute-force attacks using failed login attempt limitation.
- To protect the dashboard using session-based authentication.
- To use safe login error messages.
- To document vulnerabilities, impact, and fixes in a security report.

---

## 3. Scope of Testing

This project was tested only in a local development environment.

The testing was performed on the local system using:

```text
http://127.0.0.1:5000
```

This project is created only for educational and defensive security learning purposes.

### Application Features Tested

- User registration
- User login
- Dashboard access
- Logout
- Invalid login attempts
- Failed login attempt lock
- Session-based authentication
- Password hashing
- SQL injection prevention

---

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Flask | Web framework |
| SQLite | Database |
| HTML | Page structure |
| CSS | Page styling |
| Werkzeug Security | Password hashing and verification |
| GitHub | Project hosting and documentation |

---

## 5. Project Description

The Secure Login System is a web application that allows users to register, login, access a dashboard, and logout.

The application includes important security features such as password hashing, SQL injection prevention, failed login attempt limitation, session validation, session timeout, and safe login error messages.

### Main Project Files

```text
secure-login-system/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
│
├── static/
│   └── style.css
│
├── screenshots/
│   ├── 01-register-page.png
│   ├── 02-login-page.png
│   ├── 03-invalid-login.png
│   ├── 04-account-locked.png
│   └── 05-dashboard-success.png
│
└── docs/
    └── SECURITY_REPORT.md
```

---

## 6. Vulnerability 1: Plain Text Password Storage

### Issue

In weak login systems, passwords may be stored directly in the database as plain text.

Example of weak password storage:

```text
username: mithra
password: mithra123
```

This is unsafe because anyone who gets database access can directly read the user password.

### Impact

If passwords are stored in plain text and the database is leaked, attackers can directly access user passwords.

This can cause:

- Account compromise
- Unauthorized login
- Data theft
- Password reuse attacks on other websites

### Fix Implemented

This project stores passwords using hashing.

Password hashing converts the original password into a different unreadable format before storing it in the database.

### Secure Code Used

During registration, the password is hashed before storing:

```python
hashed_password = generate_password_hash(password)
```

During login, the entered password is compared with the hashed password:

```python
check_password_hash(user["password"], password)
```

### Result

The actual password is not stored in the database. Only the hashed version of the password is stored.

This improves password security.

---

## 7. Vulnerability 2: SQL Injection

### Issue

SQL injection is a web security vulnerability that happens when user input is directly added into an SQL query.

Example of unsafe query:

```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
```

This is dangerous because attackers may enter SQL commands as input.

### Impact

SQL injection can allow attackers to:

- Bypass login
- Access unauthorized data
- Modify database records
- Delete database records
- Damage application security

### Fix Implemented

This project uses parameterized queries.

Parameterized queries separate SQL code from user input. This means user input is treated only as data, not as part of the SQL command.

### Secure Code Used

For login:

```python
user = connection.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
).fetchone()
```

For registration:

```python
connection.execute(
    "INSERT INTO users (username, password, failed_attempts) VALUES (?, ?, ?)",
    (username, hashed_password, 0)
)
```

For updating failed attempts:

```python
connection.execute(
    "UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?",
    (username,)
)
```

### Result

User input is handled safely. This helps prevent SQL injection attacks.

---

## 8. Vulnerability 3: Brute Force Login Attempts

### Issue

A brute-force attack happens when an attacker repeatedly tries different passwords until the correct password is found.

If a login system allows unlimited wrong attempts, attackers can keep guessing passwords.

### Impact

Brute-force attacks can lead to:

- Unauthorized account access
- Password guessing
- Account compromise
- Security risk for users

### Fix Implemented

This project counts failed login attempts.

If a user enters the wrong password 3 times, the account is temporarily locked.

### Secure Code Used

Checking failed attempts:

```python
if user["failed_attempts"] >= 3:
    message = "Account temporarily locked due to too many failed attempts."
```

Increasing failed attempt count:

```python
connection.execute(
    "UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?",
    (username,)
)
```

Resetting failed attempts after correct login:

```python
connection.execute(
    "UPDATE users SET failed_attempts = 0 WHERE username = ?",
    (username,)
)
```

### Result

After 3 wrong login attempts, the account is temporarily locked.

This reduces the risk of brute-force password guessing.

---

## 9. Vulnerability 4: Weak Login Error Messages

### Issue

Some login systems reveal too much information through error messages.

Bad examples:

```text
Username does not exist.
```

```text
Password is wrong.
```

These messages are unsafe because they help attackers find valid usernames.

### Impact

Attackers can use detailed error messages to identify existing usernames.

This is called username enumeration.

### Fix Implemented

This project uses a common error message for both wrong username and wrong password.

### Secure Message Used

```text
Invalid username or password.
```

### Result

The application does not reveal whether the username is wrong or the password is wrong.

This improves login security.

---

## 10. Vulnerability 5: Session Mismanagement

### Issue

After login, the application must remember that the user is authenticated.

If session checking is not implemented, unauthorized users may access protected pages like the dashboard.

### Impact

Poor session management can cause:

- Unauthorized dashboard access
- Account misuse
- Privacy issues
- Weak authentication control

### Fix Implemented

This project uses Flask sessions to manage logged-in users.

The dashboard page checks whether the user is logged in before allowing access.

### Secure Code Used

```python
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])
```

### Result

Only logged-in users can access the dashboard page.

If a user tries to access the dashboard without login, they are redirected to the login page.

---

## 11. Vulnerability 6: Long Active Sessions

### Issue

If a session stays active for a long time, someone else may use the same system and access the account.

This is risky on shared or public computers.

### Impact

Long active sessions can cause:

- Unauthorized access
- Account misuse
- Privacy risk
- Security issues on shared systems

### Fix Implemented

This project uses session timeout.

The session expires after a limited time.

### Secure Code Used

```python
app.permanent_session_lifetime = timedelta(minutes=10)
```

After successful login:

```python
session.permanent = True
session["username"] = username
```

### Result

The session expires after 10 minutes.

This reduces the risk of unauthorized access on shared systems.

---

## 12. Security Features Implemented

| Security Feature | Status |
|---|---|
| Password hashing | Implemented |
| SQL injection prevention | Implemented |
| Failed login attempt limitation | Implemented |
| Session-based authentication | Implemented |
| Session timeout | Implemented |
| General login error message | Implemented |
| Logout function | Implemented |
| Dashboard access protection | Implemented |

---

## 13. Testing Performed

### Test Case 1: User Registration

| Field | Description |
|---|---|
| Test Objective | Check whether a new user can register |
| Input | New username and password |
| Expected Result | User account should be created |
| Actual Result | User account created successfully |
| Status | Passed |

---

### Test Case 2: Valid Login

| Field | Description |
|---|---|
| Test Objective | Check whether valid users can login |
| Input | Correct username and password |
| Expected Result | User should be redirected to dashboard |
| Actual Result | Dashboard opened successfully |
| Status | Passed |

---

### Test Case 3: Invalid Login

| Field | Description |
|---|---|
| Test Objective | Check error message for wrong login |
| Input | Wrong username or password |
| Expected Result | Error message should be displayed |
| Actual Result | Invalid username or password message displayed |
| Status | Passed |

---

### Test Case 4: Failed Attempt Lock

| Field | Description |
|---|---|
| Test Objective | Check account lock after failed attempts |
| Input | Wrong password entered 3 times |
| Expected Result | Account should be temporarily locked |
| Actual Result | Account locked message displayed |
| Status | Passed |

---

### Test Case 5: Dashboard Without Login

| Field | Description |
|---|---|
| Test Objective | Check protected dashboard access |
| Input | Open dashboard URL without login |
| Expected Result | User should be redirected to login page |
| Actual Result | User redirected to login page |
| Status | Passed |

---

### Test Case 6: Logout

| Field | Description |
|---|---|
| Test Objective | Check logout functionality |
| Input | Click logout |
| Expected Result | Session should be cleared and user should return to login page |
| Actual Result | Logout worked successfully |
| Status | Passed |

---

## 14. Screenshots Included

The following screenshots are included in the project repository:

```text
screenshots/01-register-page.png
screenshots/02-login-page.png
screenshots/03-invalid-login.png
screenshots/04-account-locked.png
screenshots/05-dashboard-success.png
```

These screenshots show the working application pages and security-related outputs.

---

## 15. Limitations

This is a beginner-level educational project. Some advanced production-level security features are not included.

Current limitations:

- No email verification
- No forgot password feature
- No CAPTCHA
- No automatic unlock after fixed time
- No CSRF protection
- No HTTPS because it is tested locally
- No advanced logging system
- Secret key is written directly in the code for learning purpose

---

## 16. Future Improvements

The project can be improved by adding:

- Password strength validation
- Email verification
- Forgot password and reset password feature
- CAPTCHA after multiple failed login attempts
- Automatic unlock after a fixed time
- CSRF protection
- HTTPS in production
- Environment variables for secret key
- Security event logging
- Admin panel for user management

---

## 17. Conclusion

This project demonstrates how a simple login system can be improved using secure coding practices.

The main security improvements implemented in this project are:

- Password hashing
- SQL injection prevention
- Failed login attempt limitation
- Session validation
- Session timeout
- Safe login error messages
- Logout functionality

This project helped me understand both software development and basic web application security concepts. It also helped me learn how to document vulnerabilities, impact, fixes, and testing results in a professional security report.

---

## 18. Disclaimer

This project is created for educational and defensive security learning purposes only.

Testing should be performed only in a local lab environment or on systems where proper permission is given.

This project should not be used for attacking or testing real websites without authorization.