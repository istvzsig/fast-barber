from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List

from pathlib import Path

from package.crud import get_available_hours, set_available_hours
from package.dependencies import get_db
from package.models import Barber, Booking, User
from package.schemas import AvailableHoursCreate, AvailableHoursResponse, BarberCreate, BookingCreate

app = FastAPI()

templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent / "templates")
)

app.mount("/static", StaticFiles(directory="static"), name="static")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/barbers/")
def create_barber(barber: BarberCreate, db: Session = Depends(get_db)):
    new_barber = Barber(name=barber.name)
    db.add(new_barber)
    db.commit()
    return new_barber


@app.get("/barbers/", response_model=List[BarberCreate])
def list_barbers(db: Session = Depends(get_db)):
    return db.query(Barber).all()


@app.post("/barbers/{barber_id}/available_hours/")
def add_available_hours(barber_id: int, available_hours: list[AvailableHoursCreate], db: Session = Depends(get_db)):
    set_available_hours(db, barber_id, available_hours)
    return {"message": "Available hours set successfully"}


@app.get("/barbers/{barber_id}/available_hours/", response_model=list[AvailableHoursResponse])
def fetch_available_hours(barber_id: int, db: Session = Depends(get_db)):
    return get_available_hours(db, barber_id)


@app.get("/bookings/")
def get_bookings(request: Request, db: Session = Depends(get_db)):
    barbers = db.query(Barber).all()

    bookings = reversed(db.query(Booking).all())
    formatted_bookings = []
    for booking in bookings:
        user = db.query(User).filter(User.id == booking.user_id).first()
        barber = db.query(Barber).filter(
            Barber.id == booking.barber_id).first()
        formatted_bookings.append(
            {
                "user_name": user.username if user else "Unknown",
                "barber_name": barber.name if barber else "Unknown",
                "appointment_time": booking.appointment_time,
            }
        )

    return templates.TemplateResponse(
        "bookings.html",
        {"request": request, "bookings": formatted_bookings, "barbers": barbers},
    )


@app.post("/bookings/")
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == booking.username).first()
    if not user:
        user = User(username=booking.username, hashed_password="fakehash")
        db.add(user)
        db.commit()
        db.refresh(user)

    new_booking = Booking(
        user_id=user.id,
        barber_id=booking.barber_id,
        appointment_time=booking.appointment_time,
    )
    db.add(new_booking)
    db.commit()
    return {"message": "Booking successful"}
