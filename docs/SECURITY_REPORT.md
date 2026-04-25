# Security Report

## Project Name
Secure Login System with Vulnerability Fixes

## Objective
The objective of this project is to build a basic login system and improve it using secure coding practices.  
This project demonstrates common authentication vulnerabilities and explains how they can be fixed in a simple Flask and SQLite application.

---

## Scope of Testing

This project was tested only in a local development environment.

### Application Features Tested
- User registration
- User login
- Dashboard access
- Logout
- Failed login attempts
- Session-based authentication

### Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS
- Werkzeug Security

---

## Vulnerability 1: Plain Text Password Storage

### Issue
In many weak login systems, passwords are stored directly in the database as plain text.

Example of weak storage:

```text
username: admin
password: admin123