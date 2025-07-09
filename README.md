📚 Library Service API

Project Description

A RESTful web application for managing a digital library system. 
Users can browse books, borrow them if available, and return them. 
Admins can manage books and monitor borrowings. JWT-based authentication ensures secure access.

Features

🔐 JWT authentication for secure API access

📘 API documentation via:

/api/schema/swagger-ui/ (Swagger UI)

/api/schema/redoc/ (ReDoc)

📚 Public book listing and detail view

🛠 Admin-only book creation, update, and deletion

📖 Borrow books with inventory checks

🔁 Return books via custom return_book endpoint

🔍 Borrowings filtering:

is_active=true/false to filter by return status

user_id=<id> filter available for admin users

👤 Users can view only their own borrowings (unless admin)

Technologies Used

Backend: Django 5.x

Database: SQLite (or PostgreSQL)

API: Django REST Framework, JWT (SimpleJWT), drf-spectacular

Testing: unittest (TestCase) + coverage.py

Filtering: django-filter

API Documentation

Swagger UI: http://localhost:8000/api/schema/swagger-ui/

ReDoc: http://localhost:8000/api/schema/redoc/