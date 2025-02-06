from datetime import datetime, time
from pydantic import BaseModel
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    password: str


class BarberCreate(BaseModel):
    name: str


class BarberResponse(BarberCreate):
    id: int
    available_hours: List["AvailableHoursResponse"] = []

    class Config:
        orm_mode = True


class BookingCreate(BaseModel):
    username: str
    barber_id: int
    appointment_time: datetime


class TokenData(BaseModel):
    username: Optional[str] = None


class AvailableHoursCreate(BaseModel):
    barber_id: int
    day_of_week: str
    start_time: time
    end_time: time


class AvailableHoursResponse(AvailableHoursCreate):
    id: int

    class Config:
        orm_mode = True
