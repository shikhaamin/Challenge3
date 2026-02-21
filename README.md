# Hackathon Backend API

This repository contains a basic FastAPI backend that connects to a SQL database with two main tables:

- **employees** – store employee information (id, name)
- **tasks** – tasks assigned to employees (id, title, start_time, end_time, employee_id)

## Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**
   ```bash
   uvicorn MainAPI:app --reload
   ```

   The API will be reachable at `http://127.0.0.1:8000` and the automatic docs are available at `/docs` (Swagger UI) and `/redoc`.

## Database

By default the app uses a SQLite database file named `hackathon.db` located in the project root. You can change the connection string in `database.py` to use PostgreSQL, MySQL, etc.

## Available Endpoints

### Employees
- `POST /employees/` – create a new employee (`name`)
- `GET /employees/` – list employees (supports `skip` and `limit` query parameters)
- `GET /employees/{employee_id}` – retrieve one employee by ID (includes tasks)

### Tasks
- `POST /tasks/` – create a task (`employee_id`, `title`, `start_time`, `end_time`)
- `GET /tasks/` – list tasks
- `GET /employees/{employee_id}/tasks/` – list tasks for a specific employee

The Pydantic schemas are defined in `schemas.py`, and the SQLAlchemy models are in `models.py`.

## Notes
- The API currently implements only basic CRUD and does not include authentication.
- Additional endpoints (update, delete, user-specific queries) can be added as needed.

---

Feel free to modify the schema or add business logic for your hackathon frontend.