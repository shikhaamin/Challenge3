from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_availabilities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Availability).offset(skip).limit(limit).all()


def create_availability(db: Session, availability: schemas.AvailabilityCreate):
    db_avail = models.Availability(
        user_id=availability.user_id,
        start_time=availability.start_time,
        end_time=availability.end_time,
        is_available=availability.is_available,
    )
    db.add(db_avail)
    db.commit()
    db.refresh(db_avail)
    return db_avail


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
