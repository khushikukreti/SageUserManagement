from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user_model import User, UserCreate
from app.dependencies.hashing import hash_password

class UserService:
    def create_user(self, user: UserCreate, db: Session()) -> bool:
        # db = Session()
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            return False
        hashed_password = hash_password(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return True
