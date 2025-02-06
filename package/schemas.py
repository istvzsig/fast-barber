from pydantic import BaseModel
from datetime import datetime


class BarberCreate(BaseModel):
    name: str


class BookingCreate(BaseModel):
    username: str
    barber_id: int
    appointment_time: datetime  # This expects the full datetime format


class AvailableHoursCreate(BaseModel):
    day_of_week: str
    start_time: str
    end_time: str
