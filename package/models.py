from sqlalchemy import Time, create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from package.helpers import get_database_url

engine = create_engine(get_database_url(), connect_args={
                       "check_same_thread": False})
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Barber(Base):
    __tablename__ = "barbers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    available_hours = relationship(
        "AvailableHours", back_populates="barber", cascade="all, delete")


class AvailableHours(Base):
    __tablename__ = "available_hours"
    id = Column(Integer, primary_key=True, index=True)
    barber_id = Column(Integer, ForeignKey("barbers.id"))
    day_of_week = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    barber = relationship("Barber", back_populates="available_hours")


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    barber_id = Column(Integer, ForeignKey("barbers.id"))
    appointment_time = Column(Time)


def create_tables():
    print("🗄️ Creating database tables if they do not exist...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database setup completed.")


create_tables()
