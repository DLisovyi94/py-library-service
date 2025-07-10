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

Containerization: Docker, Docker Compose

📚 Public book listing and detail view

🛠 Admin-only book creation, update, and deletion

📖 Borrow books with inventory checks

🔁 Return books via custom return_book endpoint

🔍 Borrowings filtering:

is_active=true/false to filter by return status

user_id= filter available for admin users

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

Installation (Local Development)

Prerequisites

- Python 3.10+  
- Docker & Docker Compose

1. Clone the repository

bash
git clone https://github.com/your-username/train-station-api.git
cd train-station-api

2. Create and activate a virtual environment

python -m venv .venv
source .venv/bin/activate  # For Linux/macOS
or
.venv\Scripts\activate  # For Windows

3. Install dependencies

pip install -r requirements.txt

4. Create a `.env` file

cp env.sample .env

Fill in required environment variables in `.env`, for example:


POSTGRES_USER=library_service
POSTGRES_PASSWORD=library_service
POSTGRES_DB=library_service
POSTGRES_HOST=db
POSTGRES_PORT=5432
DEBUG=True
SECRET_KEY=your-secret-key

Important: "POSTGRES_HOST" should match the name of the service in "docker-compose.yml" ("db").

5. Start the PostgreSQL container

docker-compose up -d db

6. Apply database migrations

python manage.py migrate

7. Create a superuser (for Django Admin)

python manage.py createsuperuser

8. Run the development server


python manage.py runserver

9. (Optional) Load sample data

python manage.py loaddata full_data.json

Containerized Deployment

To run the entire project in Docker (backend + database):

docker-compose up --build
