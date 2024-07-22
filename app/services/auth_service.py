import re

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas.user_schema import UserCreate, UserResponse
from app.utils.hashing import hash_password, verify_password
from app.db.database import get_db
import app.config.develop as config
import requests

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

# Function to create access token
def create_access_token(data: dict):
    """
        Generates a JWT (JSON Web Token) for user authentication.

        Args:
        data (dict): A dictionary containing payload data that will be encoded into the JWT.
                     Typically, this includes user identification information such as user ID.

        Returns:
        str: A string representing the JWT encoded with the provided data and additional claims.

        This function takes user data, copies it to prevent modification of the original data,
        and adds an expiration claim based on a predefined duration (ACCESS_TOKEN_EXPIRE_MINUTES).
        It then encodes this information into a JWT using a secret key and a specified algorithm.

        The resulting token can be used to authenticate API requests, ensuring that they are coming
        from valid and authorized users.

        Example:
        To create a token with user identification:
        user_data = {"sub": user_id}
        access_token = create_access_token(data=user_data)
        print(access_token)
        The 'sub' field is commonly used to represent the subject of the token (the user it identifies).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to authenticate user
def authenticate_user(db, email: str, password: str):
    """
        Authenticates a user by verifying their email and password.

        Args:
        db: The database connection where user data is stored.
        email (str): The email address of the user attempting to log in.
        password (str): The password provided by the user for login.

        Returns:
        tuple or bool: Returns a tuple containing user data if authentication is successful, otherwise False.

        This function performs user authentication by executing a SQL query to retrieve the user's stored data
        based on the provided email. It then uses the `verify_password` function to check if the provided password
        matches the stored hashed password. If the authentication is successful, it returns the user's data;
        otherwise, it returns False, indicating authentication failure.

        The function handles the following steps:
        - Executes a SQL query to fetch the user's data from the database.
        - Checks if the user exists and if the provided password matches the stored hashed password.
        - Returns the user's data if authentication is successful, or False if it fails.

        Example usage:
        db_connection = get_db_connection()
        user_credentials = authenticate_user(db_connection, "user@example.com", "password123")
        if user_credentials:
            print("Authentication successful!")
        else:
            print("Authentication failed.")
        Note: This function assumes the existence of a `verify_password` function that takes a plain password and
        a hashed password, returning True if they match, and False otherwise.
    """
    db.execute("SELECT id, email, hashed_password, role FROM users WHERE email = %s", (email,))
    user = db.fetchone()
    if not user or not verify_password(password, user[2]):
        return False
    return user

def validate_password(password: str):
    """
    Validate the given password based on multiple criteria.

    Args:
    password (str): The password string to be validated.

    Raises:
    HTTPException: If the password does not meet the required criteria.

    Criteria:
    1. The password must be between 6 and 8 characters long.
    2. The password must contain at least one uppercase letter.
    3. The password must contain at least one lowercase letter.
    4. The password must contain at least one special character from the set [!@#$%^&*(),.?":{}|<>].

    Example usage:
    # >>> validate_password("Pass!w")
    Raises HTTPException with status code 400 and detail "Password must be between 6 and 8 characters long"
    # >>> validate_password("Password!")
    Raises HTTPException with status code 400 and detail "Password must be between 6 and 8 characters long"
    # >>> validate_password("Pass!")
    Raises HTTPException with status code 400 and detail "Password must contain at least one uppercase letter"
    # >>> validate_password("pass!")
    Raises HTTPException with status code 400 and detail "Password must contain at least one lowercase letter"
    # >>> validate_password("Passw")
    Raises HTTPException with status code 400 and detail "Password must contain at least one special character"
    """

    # Check if the password length is between 6 and 8 characters
    if len(password) < 6 or len(password) > 8:
        raise HTTPException(status_code=400, detail="Password must be between 6 and 8 characters long")

    # Check for at least one uppercase letter in the password
    if not re.search(r'[A-Z]', password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")

    # Check for at least one lowercase letter in the password
    if not re.search(r'[a-z]', password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")

    # Check for at least one special character in the password
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character")


# Function to register user
def register_user(db, user: UserCreate):
    """
        Registers a new user in the database.

        Args:
        db: The database connection where user data is stored.
        user (UserCreate): A Pydantic model instance containing the user's email and password.

        Returns:
        UserResponse: A Pydantic model instance representing the newly created user.

        This function performs the following steps to register a new user:
        - Checks if a user with the provided email already exists in the database.
        - If the user exists, raises an HTTPException to prevent duplicate entries.
        - If the user does not exist, hashes the password and inserts the new user's details into the database.
        - Retrieves the new user's data from the database to confirm the insertion and to return it.

        Raises:
        HTTPException: An exception indicating that the user already exists, with a status code of 400.

        Example usage:
        db_connection = get_db_connection()
        new_user_data = UserCreate(email="newuser@example.com", password="securePassword123")
        try:
            registered_user = register_user(db_connection, new_user_data)
            print("User registered successfully:", registered_user)
        except HTTPException as e:
            print(e.detail)
        Note: This function assumes the existence of a `hash_password` function that takes a plain password and returns a hashed version.
    """
    # Validate the password
    validate_password(user.password)
    # Check if user already exists
    db.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    existing_user = db.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(user.password)
    db.execute("INSERT INTO users (email, hashed_password, role) VALUES (%s, %s, %s)", (user.email, hashed_password, "user"))
    new_user = db.execute("SELECT id,email,role FROM users WHERE email = %s", (user.email,)).fetchone()
    print(new_user)
    return UserResponse(id=new_user[0], email=new_user[1], role=new_user[2])

def google_login(token, db):
    """
        Authenticates a user using Google OAuth.

        Args:
        token (str): The Google OAuth token provided by the client.
        db: The database connection where user data is stored.

        Returns:
        dict: A dictionary containing the JWT access token, token type, user ID, and role ID.

        This function performs the following steps to authenticate a user via Google OAuth:
        - Verifies the Google token by making a request to Google's tokeninfo endpoint.
        - If the token is invalid, raises an HTTPException.
        - Retrieves the user's email and Google user ID from the response.
        - Checks if the user already exists in the database.
        - If the user exists, retrieves their ID and role.
        - If the user does not exist, creates a new user in the database using the email and a hashed version of the Google user ID.
        - Generates a JWT access token for the user.
        - Returns a dictionary containing the access token, token type, user ID, and role.

        Raises:
        HTTPException: An exception indicating that the Google token is invalid or user information could not be retrieved.

        Example usage:
        db_connection = get_db_connection()
        try:
            user_info = google_login("example_google_token", db_connection)
            print("User authenticated successfully:", user_info)
        except HTTPException as e:
            print(e.detail)
        Note: This function assumes the existence of `create_access_token` and `hash_password` functions.
    """
    # Verify Google token
    google_api_url = f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
    response = requests.get(google_api_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    google_data = response.json()
    google_user_id = google_data.get("sub")
    email = google_data.get("email")

    if not email or not google_user_id:
        raise HTTPException(status_code=400, detail="Unable to retrieve user information from Google")

    # Check if the user already exists
    db.execute("SELECT id, email, role FROM users WHERE email = %s", (email,))
    existing_user = db.fetchone()

    if existing_user:
        user_id = existing_user[0]
        role = existing_user[2]
    else:
        # Create user if not exists
        hashed_password = hash_password(google_user_id)  # Using Google User ID as a pseudo-password for demo
        db.execute("INSERT INTO users (email, hashed_password, role,id) VALUES (%s, %s, %s, %s)", (email, hashed_password, 'user', google_user_id))  # assuming role_id 2 for regular user
        db.execute("SELECT id, role FROM users WHERE email = %s", (email,))
        new_user = db.fetchone()
        user_id = new_user[0]
        role = new_user[1]

    # Generate JWT token
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer", "id": user_id, "role_id": role}
