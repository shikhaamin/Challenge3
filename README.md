
# Overall Project Description:
- This project is a centralized platform designed to track team availability in real time and provide intelligent task reassignment suggestions to keep projects on schedule.

The current code implements the backend API layer in Python, which:

Exposes endpoints to retrieve team member information, task details, and availability status.

Calculates workload and identifies overloaded users.

Suggests potential task reassignments based on availability and capacity.

At this stage, the API uses mock data to simulate database responses, allowing the frontend to interact with realistic data structures and test the reassignment logic. Integration with the SQL database and real-time calendar data will be added in the next development phase.



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


