from fastapi import APIRouter

from .barbers import router as barbers_router
from .bookings import router as bookings_router

api_router = APIRouter()

api_router.include_router(barbers_router, prefix="/barbers", tags=["barbers"])
api_router.include_router(
    bookings_router, prefix="/bookings", tags=["bookings"])
