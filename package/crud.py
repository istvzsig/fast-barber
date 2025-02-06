from sqlalchemy.orm import Session
from package.models import Barber, AvailableHours


def set_available_hours(db: Session, barber_id: int, available_hours: list):
    for hour in available_hours:
        available_hour = AvailableHours(
            barber_id=barber_id,
            day_of_week=hour.day_of_week,
            start_time=hour.start_time,
            end_time=hour.end_time,
        )
        db.add(available_hour)
    db.commit()


def get_available_hours(db: Session, barber_id: int):
    return db.query(AvailableHours).filter(AvailableHours.barber_id == barber_id).all()
