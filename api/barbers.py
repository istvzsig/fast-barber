from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from package.models import Barber
from package.schemas import BarberCreate
from db.database import get_db

router = APIRouter()


@router.post("/")
def create_barber(barber: BarberCreate, db: Session = Depends(get_db)):
    new_barber = Barber(name=barber.name)
    db.add(new_barber)
    db.commit()
    return new_barber


@router.get("/", response_model=List[BarberCreate])
def list_barbers(db: Session = Depends(get_db)):
    return db.query(Barber).all()
