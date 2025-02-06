from sqlalchemy.orm import Session
from .models import User, Barber, Booking
from .schemas import UserCreate, BarberCreate, BookingCreate


def create_user(db: Session, user: UserCreate):
    # Hash password here
    db_user = User(username=user.username, hashed_password="fakehash")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_barber(db: Session, barber: BarberCreate):
    new_barber = Barber(name=barber.name)
    db.add(new_barber)
    db.commit()
    return new_barber


def get_barbers(db: Session):
    return db.query(Barber).all()


def create_booking(db: Session, booking: BookingCreate):
    user = db.query(User).filter(User.username == booking.username).first()
    if not user:
        user = create_user(db, UserCreate(
            username=booking.username, password="fakehash"))
    new_booking = Booking(user_id=user.id, barber_id=booking.barber_id,
                          appointment_time=booking.appointment_time)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking
