from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas.user_schema import UserCreate, UserResponse
from app.utils.hashing import hash_password, verify_password
from app.db.database import get_db
import app.config.develop as config

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

# Function to create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to authenticate user
def authenticate_user(db, email: str, password: str):
    db.execute("SELECT id, email, hashed_password, role FROM users WHERE email = %s", (email,))
    user = db.fetchone()
    if not user or not verify_password(password, user[2]):
        return False
    return user

# Function to register user
def register_user(db, user: UserCreate):
    # Check if user already exists
    db.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    existing_user = db.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(user.password)
    db.execute("INSERT INTO users (email, hashed_password, role) VALUES (%s, %s, %s)", (user.email, hashed_password, "user"))
    # db.commit()
    new_user = db.execute("SELECT id,email,role FROM users WHERE email = %s", (user.email,)).fetchone()
    print(new_user)
    return UserResponse(id=new_user[0], email=new_user[1], role=new_user[2])
