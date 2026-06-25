# AI Job Tracker

AI Job Tracker is a FastAPI-based backend application that helps users manage job applications, upload resumes, analyze resume-job matches, and track job search progress.

## Features

- User signup and login
- JWT-based authentication
- Protected user profile route
- Job tracking
- Resume PDF upload
- Resume text extraction from PDFs
- Resume-job match analysis
- Dashboard statistics
- PostgreSQL database integration
- Alembic database migrations

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT authentication
- Passlib + bcrypt
- PyMuPDF
- Uvicorn
- Git + GitHub

## Project Structure

```txt
ai-job-tracker/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── alembic/
├── uploads/
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md