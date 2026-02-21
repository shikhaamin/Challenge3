from fastapi.testclient import TestClient
from MainAPI import app

client = TestClient(app)

# create user
r = client.post("/users/", json={"name":"Test User","email":"test@example.com"})
print("POST /users/ ->", r.status_code, r.json())

# list users
r = client.get("/users/")
print("GET /users/ ->", r.status_code, r.json())