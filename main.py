from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from typing import List

from pathlib import Path

from package.dependencies import get_db
from package.helpers import create_access_token, get_database_url, get_password_hash, verify_password
from package.models import Barber, Booking, User
from package.schemas import BarberCreate, BookingCreate, UserCreate

# FastAPI app
app = FastAPI()

# Set up templates directory
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Authentication
@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(pwd_context, user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Barber Routes
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

# Booking Routes
@app.get("/bookings/")
def get_bookings(request: Request, db: Session = Depends(get_db)):
    # Get all barbers
    barbers = db.query(Barber).all()

    # Get existing bookings
    bookings = reversed(db.query(Booking).all())
    formatted_bookings = []
    for booking in bookings:
        user = db.query(User).filter(User.id == booking.user_id).first()
        barber = db.query(Barber).filter(Barber.id == booking.barber_id).first()
        formatted_bookings.append({
            "user_name": user.username if user else "Unknown",
            "barber_name": barber.name if barber else "Unknown",
            "appointment_time": booking.appointment_time
        })

    return templates.TemplateResponse("bookings.html", {
        "request": request, 
        "bookings": formatted_bookings,
        "barbers": barbers
    })

@app.post("/bookings/")
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    # Check if the user exists, otherwise create one
    user = db.query(User).filter(User.username == booking.username).first()
    if not user:
        user = User(username=booking.username, hashed_password="fakehash")  # No real password needed
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create a new booking
    new_booking = Booking(
        user_id=user.id,
        barber_id=booking.barber_id,
        appointment_time=booking.appointment_time
    )
    db.add(new_booking)
    db.commit()
    return {"message": "Booking successful"}