# JobTrack — Job Application Management System

A full-stack portfolio project for organizing a job search. Built with React, JavaScript, Python Flask, Flask-JWT-Extended, SQLAlchemy, and MySQL.

## Features

- Register/login with hashed passwords and expiring JWT access tokens
- User-specific data access: one account cannot read, edit, or delete another user's applications
- Create, view, update, and delete job applications
- Track Applied, Assessment, Interview, Selected, and Rejected statuses
- Search by company, role, or location; filter by status; sort by date, company, status, or salary
- Dashboard statistics calculated from the database
- Input validation for required fields, dates, salary values, status, and job URLs
- Responsive UI, loading states, and actionable error messages
- API health endpoint and automated backend tests

## Technology stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| API | Python, Flask, REST, Flask-CORS |
| Authentication | Flask-JWT-Extended, Werkzeug password hashing |
| Data layer | Flask-SQLAlchemy, SQLAlchemy ORM |
| Database | MySQL 8+ / PyMySQL |
| Testing | pytest, Flask test client, SQLite in-memory test database |

## Requirements

- Python 3.10 or newer
- Node.js 22.12+ recommended for the Vite toolchain
- MySQL 8+ running locally
- Git (recommended)

## Run locally on Windows

Open **three terminals** in VS Code: one for MySQL (or your MySQL client), one for the backend, and one for the frontend.

### 1. Create the database

Open MySQL Workbench or the MySQL command line and run:

```sql
CREATE DATABASE job_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configure and start the backend

```powershell
cd job_application_management_system\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `backend/.env` and set the correct MySQL password. Replace the example JWT secret with a long, random secret. For local development, the file should contain values similar to:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost/job_tracker
JWT_SECRET_KEY=put-a-long-random-secret-here
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
FLASK_DEBUG=true
HOST=127.0.0.1
PORT=5000
```

If your MySQL password contains URL-special characters (such as `@`, `#`, `/`, or `:`), URL-encode those characters in `DATABASE_URL`.

Start Flask:

```powershell
python app.py
```

Verify the backend in your browser: `http://127.0.0.1:5000/` and `http://127.0.0.1:5000/api/health`. The health endpoint should return `{"status":"ok","database":"connected"}`.

### 3. Start the frontend

In a **new terminal** from the project root:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open the Vite URL printed in the terminal, normally `http://localhost:5173`.

Keep both backend and frontend terminals running while using the app. If Firefox says it cannot connect to `127.0.0.1:5000`, the Flask process is not running, stopped with an error, or is listening on a different port. Read the backend terminal first.

## Run automated backend tests

The tests use a temporary in-memory SQLite database, so they do not need your local MySQL database. From the backend directory with the virtual environment activated:

```powershell
python -m pytest -q
```

The suite checks authentication, duplicate/weak-password handling, application CRUD, validation, dashboard counts, and access isolation between users.

## API reference

Base URL: `http://127.0.0.1:5000/api`

| Method | Endpoint | Authentication |
|---|---|---|
| POST | `/auth/register` | No |
| POST | `/auth/login` | No |
| GET | `/auth/me` | JWT required |
| GET | `/applications` | JWT required |
| POST | `/applications` | JWT required |
| GET | `/applications/<id>` | JWT required |
| PUT | `/applications/<id>` | JWT required |
| DELETE | `/applications/<id>` | JWT required |
| GET | `/applications/stats` | JWT required |
| GET | `/health` | No |

For protected endpoints, send `Authorization: Bearer <token>`. Application list query parameters: `search`, `status`, `sort` (`applied_date`, `company`, `status`, `salary`), and `order` (`asc`, `desc`).

Example application request:

```json
{
  "company": "Example Technologies",
  "job_role": "Associate Engineer",
  "location": "Pune",
  "applied_date": "2026-10-10",
  "salary": 600000,
  "job_link": "https://example.com/careers/role",
  "status": "Applied"
}
```

## Suggested GitHub workflow

1. Create a repository with a clear description and add this README.
2. Run the app and tests locally before committing.
3. Commit small, meaningful changes, for example `Add application validation` or `Add API tests`.
4. Add screenshots/GIFs of registration, dashboard, filters, and the application form to the repository README.
5. Never commit `backend/.env`, virtual environments, `frontend/node_modules`, access tokens, or real user data.

## Production-readiness notes

This is a portfolio/local-development project, not a fully audited production service. Before public deployment, use HTTPS, a managed database, a strong secret stored in the hosting provider's environment settings, restricted CORS origins, database migrations (for example Flask-Migrate/Alembic), rate limiting on authentication routes, security monitoring, and a deployment configuration that disables debug mode. `db.create_all()` is convenient for a learning project; migrations are preferred for ongoing production schema changes.

## Resume description

**JobTrack — Job Application Management System | React, Flask, MySQL, REST API**

- Built a full-stack application tracker with React and Flask REST APIs backed by MySQL.
- Implemented JWT authentication, password hashing, and user-scoped CRUD operations.
- Added search, status filtering, sorting, input validation, and dashboard statistics.
- Wrote automated API tests covering authentication, CRUD workflows, validation, and cross-user access isolation.

Only list the testing/security features on your resume after you have run the tests and personally verified the behavior.
