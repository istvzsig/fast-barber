from pydantic import BaseModel
from datetime import datetime


class BarberCreate(BaseModel):
    name: str


class BarberResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    username: str
    barber_id: int
    appointment_time: datetime


class AvailableHoursCreate(BaseModel):
    day_of_week: str
    start_time: str
    end_time: str
