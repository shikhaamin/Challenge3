from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class AvailabilityBase(BaseModel):
    start_time: datetime
    end_time: datetime
    is_available: bool = True


class AvailabilityCreate(AvailabilityBase):
    user_id: int


class Availability(AvailabilityBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    user_id: int


class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    availabilities: List[Availability] = []
    tasks: List[Task] = []

    class Config:
        orm_mode = True
