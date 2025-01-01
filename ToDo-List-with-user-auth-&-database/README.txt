Try It On: https://hemanggour.pythonanywhere.com

# Flask To-Do List Server with User Authentication and Security

## Overview
This project is a Flask-based server application for managing a To-Do List with a focus on user authentication and session handling. The system allows multiple users to securely log in, create, update, and manage tasks, with robust session management. If a user logs in through the same browser with a different account, the previous session is logged out, but it remains active in other browsers or tabs.

## Features
User Authentication: Secure registration and login with session management.

## Session Handling:
Users can log in from multiple browsers or tabs simultaneously.
Logging in with another user on the same browser logs out the previous session in that browser, while other sessions remain active.

To-Do List Management: Authenticated users can create, update, and delete tasks.

## Security Measures:
Password hashing using secure cryptographic methods.
CSRF protection for form submissions.
Prevention of session hijacking and basic security against XSS.

## MySQL Database Integration: Persistent storage of users and tasks using a MySQL database.
Installation
Prerequisites
Ensure the following are installed on your system:

Python 3.x
Flask
MySQL Connector
MySQL Server installed and running
Setup

## Clone the repository:

>> git clone https://github.com/Hemanggour/Python-Server-Database-Projects/tree/main/ToDo-List-with-user-auth-%26-database

## Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install dependencies:

> pip install -r requirements.txt

## Set up your MySQL database:

Create a new database (e.g., todo_db).
Update your database connection settings in your application configuration.
You can configuration in database/db.py:

## Run the server:
> python2 main.py

The app will run by default on http://localhost:5000.

API Endpoints
User Authentication
POST /register: Register a new user.

Request: {"username": "yourname", "password": "yourpassword"}
Response: {"message": "User registered successfully"}
POST /login: Log in a user.

Request: {"username": "yourname", "password": "yourpassword"}
Response: {"message": "Logged in successfully", "session": "<session details>"}
POST /logout: Log out the current user from the active session.

Response: {"message": "Logged out successfully"}
To-Do List Management
GET /tasks: Retrieve all tasks for the authenticated user.

Response: [{"id": 1, "task": "Do laundry", "completed": false}, ...]
POST /tasks: Create a new task.

Request: {"task": "New Task"}
Response: {"id": 2, "message": "Task created successfully"}
PUT /tasks/
: Update an existing task.

Request: {"task": "Updated Task", "completed": true}
Response: {"message": "Task updated successfully"}
DELETE /tasks/
: Delete a task.

Response: {"message": "Task deleted successfully"}
Session Management
This project uses Flask sessions to manage user authentication. A few important behaviors:

## Multiple Sessions Across Browsers:
A user can log in to their account across multiple browsers or devices, and each session will remain active unless explicitly logged out.

## Single Session in the Same Browser:
If a user logs into a different account in the same browser, the previous session is automatically logged out for that browser tab but remains active in other browsers or devices.

## Session Handling:
Flask's session management stores user session data on the server-side. The server invalidates sessions when logging out from the same browser, but other sessions on different browsers or devices remain active.
Security Measures

## Password Hashing: Passwords are hashed using bcrypt (or similar) to ensure secure storage.

## Cross-Site Scripting (XSS) Protection: Input data is validated and sanitized to protect against XSS attacks.

## Session Security:
On each login, a new session is generated to prevent session fixation attacks.
Session data is stored securely in server-side storage, and session cookies are marked as HttpOnly and Secure for added protection.
Running the Application
Running the Server

## To start the server, use the following command:

> python3 main.py

## The server will run on http://localhost:5000 by default.

.
├── 
├── Database/db.py    # Database (MySQL)
├── templates/     # HTML templates
├── static/        # Static assets (CSS, images)
├── authentication.py
└── main.py        # Main server file

## Contributing
### Contributions are welcome! Please fork the repository and submit a pull request. Make sure to write tests for any new features or changes.