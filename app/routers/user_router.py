from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user_model import UserCreate
from app.services.user_service import UserService

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)

@router.post("/register")
def register_user(user: UserCreate, service: UserService = Depends(), db: Session = Depends(get_db)):
    if service.create_user(user, db):
        return {"message": "User registered successfully."}
    else:
        raise HTTPException(status_code=400, detail="Email already in use.")

# @router.post("/db_work")
# def db_work():
