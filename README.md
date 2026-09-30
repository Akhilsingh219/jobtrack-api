# JobTrack API

A backend REST API to track job applications — built with FastAPI, PostgreSQL, and JWT authentication.

## Features

- User authentication (register/login) with JWT tokens
- Passwords hashed with bcrypt
- Full CRUD for job applications (create, read, update, delete)
- Search jobs by title/company
- Pagination support
- PostgreSQL database with SQLAlchemy ORM
- Auto-generated Swagger documentation

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Auth:** JWT (python-jose) + bcrypt (passlib)
- **Validation:** Pydantic

## Setup

1. Clone the repo
```bash
   git clone https://github.com/Akhilsingh219/jobtrack-api.git
   cd jobtrack-api
```

2. Create a virtual environment and install dependencies
```bash
   python -m venv venv
   venv\Scripts\activate
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-dotenv pydantic
```

3. Create a `.env` file in the root folder: