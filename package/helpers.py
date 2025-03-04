import os
from datetime import datetime, timedelta
from jose import jwt


def get_secret_key():
    return os.getenv("SECRET_KEY", "default_secret_key")


def get_algorithm():
    return os.getenv("ALGORITHM", "default_algorithm")


def get_database_url():
    db_path = os.path.join(os.path.dirname(__file__), "../db/barbershop.db")
    return f"sqlite:///{db_path}"


def get_password_hash(context, password):
    return context.hash(password)


def verify_password(context, plain_password, hashed_password):
    return context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_secret_key(), algorithm=get_algorithm())


def parse_time_str(time_str: str) -> datetime:
    try:
        appointment_time = datetime.fromisoformat(str(time_str))
    except ValueError:
        appointment_time = datetime.combine(
            datetime.today(), datetime.strptime(str(time_str), "%H:%M:%S").time())

    return appointment_time
