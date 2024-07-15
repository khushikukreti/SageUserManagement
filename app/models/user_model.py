from sqlalchemy import Column, Integer, String
# from database import declarative_base
from pydantic import BaseModel, EmailStr, validator
import re

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):

    email: EmailStr
    password: str

    @validator('password')
    def password_validation(cls, value):
        if len(value) < 6 or len(value) > 8:
            raise ValueError('Password must be between 6-8 characters')
        if not re.search("[a-z]", value):
            raise ValueError('Password must include a lower-case letter')
        if not re.search("[A-Z]", value):
            raise ValueError('Password must include an upper-case letter')
        if not re.search("[!@#$%^&*(),.?"":{}|<>]", value):
            raise ValueError('Password must include a special character')
        return value
