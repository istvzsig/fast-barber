from pathlib import Path
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from package.models import Booking, User, Barber
from package.schemas import BookingCreate
from db.database import get_db
from package.helpers import parse_time_str

router = APIRouter()

templates = Jinja2Templates(directory=str(
    Path(__file__).resolve().parent.parent / "templates"))


@router.post("/")
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
        appointment_time=parse_time_str(booking.appointment_time),
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return {"booking": new_booking}


@router.get("/")
def get_bookings(request: Request, db: Session = Depends(get_db)):
    barbers = db.query(Barber).all()
    bookings = db.query(Booking).all()
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
        {"request": request, "bookings": formatted_bookings, "barbers": barbers}
    )
