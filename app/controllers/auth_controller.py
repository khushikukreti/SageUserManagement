import snowflake
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import authenticate_user, register_user, create_access_token, google_login
from app.db.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=['Login'], prefix='/auth')

# Manual signup endpoint
@router.post("/manual/signup", response_model=UserResponse)
def manual_signup(user: UserCreate, db:snowflake.connector.cursor = Depends(get_db)):
    """
        Handles the manual signup process for new users.

        Args:
        user (UserCreate): A Pydantic model that contains the user data for signup.
        db (Session, optional): Database session dependency, resolved by FastAPI's dependency injection system.

        Returns:
        UserResponse: A Pydantic model that defines the response structure for a successful signup.

        Raises:
        HTTPException: An exception with a status code and a detail message when user registration fails.

        This endpoint receives user data, validates it, and attempts to register the user in the database.
        If the registration is successful, it returns the user data; otherwise, it raises an HTTPException.
        """
    return register_user(db, user)

# Manual login endpoint
@router.post("/manual")
def manual_login(form_data: UserCreate, db: Session = Depends(get_db)):
    """
        Handles the manual login process for existing users.

        Args:
        form_data (UserCreate): A Pydantic model containing the email and password of the user.
        db (Session, optional): Database session dependency, resolved by FastAPI's dependency injection system.

        Returns:
        dict: A dictionary containing the access token and token type.

        Raises:
        HTTPException: An exception with a status code and a detail message for invalid credentials.

        This endpoint authenticates a user by their email and password. If authentication is successful,
        it generates a JWT access token and returns it. If authentication fails, it raises an HTTPException.
    """
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user[1]})
    return {"access_token": access_token, "token_type": "bearer"}

# Google login endpoint
@router.post("/google")
def google_oauth_login(token: str, db: Session = Depends(get_db)):
    """
        Handles the Google OAuth login process.

        Args:
        token (str): The Google OAuth token obtained from the client.
        db (Session, optional): Database session dependency, resolved by FastAPI's dependency injection system.

        Returns:
        dict: A dictionary representing the user login status or error.

        This endpoint receives a Google OAuth token, verifies it, and either logs in an existing user or registers a new one.
        It then generates a JWT token for authenticated sessions. This function is a placeholder and should be implemented
        with actual logic to handle Google OAuth tokens.
    """
    return google_login(token, db)