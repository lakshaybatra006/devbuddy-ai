from passlib.context import CryptContext
from jose import jwt
import os
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


# hash password
def hash_password(password):
    return pwd_context.hash(password)


# verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# create JWT token
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=24)

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)