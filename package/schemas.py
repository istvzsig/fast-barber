from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class BarberCreate(BaseModel):
    name: str

class BookingCreate(BaseModel):
    username: str
    barber_id: int
    appointment_time: datetime

class TokenData(BaseModel):
    username: Optional[str] = None
