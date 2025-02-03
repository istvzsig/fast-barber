from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List

from pathlib import Path

# FastAPI app
app = FastAPI()

# Set up templates directory
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database setup
DATABASE_URL = "sqlite:///./barbershop.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Barber(Base):
    __tablename__ = "barbers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    barber_id = Column(Integer, ForeignKey("barbers.id"))
    appointment_time = Column(DateTime)

Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class BarberCreate(BaseModel):
    name: str

class BookingCreate(BaseModel):
    user_id: int
    barber_id: int
    appointment_time: datetime

class TokenData(BaseModel):
    username: Optional[str] = None

class BookingCreate(BaseModel):
    username: str
    barber_id: int
    appointment_time: datetime

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper Functions
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Authentication
@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
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