import snowflake
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import authenticate_user, register_user, create_access_token
from app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Manual signup endpoint
@router.post("/manual/signup", response_model=UserResponse)
def manual_signup(user: UserCreate, db:snowflake.connector.cursor = Depends(get_db)):
    print('manual signup')
    return register_user(db, user)

# Manual login endpoint
@router.post("/manual/login")
def manual_login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user[1]})
    return {"access_token": access_token, "token_type": "bearer"}

# Google login endpoint
@router.post("/google/login")
def google_login(token: str, db: Session = Depends(get_db)):
    # Verify Google token, create user if not exists, generate JWT token
    # Placeholder for actual Google OAuth implementation
    pass
