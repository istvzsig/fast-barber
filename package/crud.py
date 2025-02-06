from sqlalchemy.orm import Session
from .models import Barber, AvailableHours
from .schemas import BarberCreate, AvailableHoursCreate


def create_barber(db: Session, barber: BarberCreate):
    new_barber = Barber(name=barber.name)
    db.add(new_barber)
    db.commit()
    db.refresh(new_barber)
    return new_barber


def get_barbers(db: Session):
    return db.query(Barber).all()


def create_available_hours(db: Session, hours: AvailableHoursCreate):
    new_hours = AvailableHours(
        barber_id=hours.barber_id,
        day_of_week=hours.day_of_week,
        start_time=hours.start_time,
        end_time=hours.end_time
    )
    db.add(new_hours)
    db.commit()
    db.refresh(new_hours)
    return new_hours


def set_available_hours(db: Session, barber_id: int, available_hours: list):
    for slot in available_hours:
        new_slot = AvailableHours(
            barber_id=barber_id,
            day_of_week=slot.day_of_week,
            start_time=slot.start_time,
            end_time=slot.end_time
        )
        db.add(new_slot)
    db.commit()


def get_available_hours(db: Session, barber_id: int):
    return db.query(AvailableHours).filter(AvailableHours.barber_id == barber_id).all()
