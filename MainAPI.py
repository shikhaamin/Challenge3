from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import engine, Base, get_db

# create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hackathon API")

# ---- users ----
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, email=user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# ---- availability ----
@app.post("/availabilities/", response_model=schemas.Availability)
def create_availability(availability: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    if crud.get_user(db, availability.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_availability(db, availability)


@app.get("/availabilities/", response_model=List[schemas.Availability])
def read_availabilities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_availabilities(db, skip=skip, limit=limit)


# ---- tasks ----
@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    if crud.get_user(db, task.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_task(db, task)


@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)
