# DevTrack

DevTrack is a Django-based study tracking and productivity web application built for learning backend engineering concepts using Python and Django.

The project focuses heavily on:

- Authentication systems
- Session management
- ORM relationships
- Form validations
- Authorization
- Secure backend development
- Clean architecture

---

# Features

## Authentication System

- User Signup
- User Login
- Secure Password Hashing
- Session-based Authentication
- Logout System

## Study Tracking

- Add study logs
- Edit study logs
- Delete study logs
- Track study hours
- Add notes and topics

## Authorization & Security

- Login protected routes
- User ownership validation
- Secure CRUD operations
- CSRF protection
- Password validation

## Backend Concepts Practiced

- Django ORM
- Aggregations
- Query filtering
- Relationships
- Middleware
- Sessions
- Form validation pipeline

---

# Tech Stack

## Backend

- Python
- Django

## Frontend

- HTML
- Bootstrap 5

## Database

- SQLite3

---

# 📂 Project Structure

```bash
devtrack/
│
├── config/
│   └── settings.py
│
├── tracker/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── manage.py
└── db.sqlite3
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/ajilaries/DevTrack.git
```

---

## Navigate to Project

```bash
cd devtrack
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

Install all dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Run Migrations (SQLite)

```bash
python manage.py makemigrations
python manage.py migrate
```

This uses SQLite at `db.sqlite3` (configured in `config/settings.py`).

---

## Start Development Server

```bash
python manage.py runserver
```

---

# Open In Browser

```text
http://127.0.0.1:8000/
```

---

# Live Demo (PythonAnywhere)

https://aries001.pythonanywhere.com/

---

# Concepts Learned

This project was built to deeply understand:

- Django Authentication
- Session Management
- Password Hashing
- Middleware
- Form Validation
- Django ORM
- CRUD Operations
- Database Relationships
- Authorization
- Secure Backend Practices

---

# 🔥 Future Improvements

- Dashboard analytics
- Charts using Chart.js
- Study streak system
- REST API integration
- User profile system
- Email verification
- Password reset system
- PostgreSQL migration
- Docker support

---

# Author

Developed by Ajil as part of backend engineering and Django learning journey.

---

# Project Goal

The main goal of DevTrack is to practice real-world backend development concepts while building a scalable Django application from scratch.
