from pydantic import BaseModel

class User(BaseModel):
    """
        Data model for user entities.

        Attributes:
        id (int): Unique identifier for the user.
        email (str): Email address of the user. This field is used for user identification and communication.
        hashed_password (str): Cryptographically hashed password for secure storage and verification.
        role (str): Role of the user within the application, determining access levels and permissions.

        The User model is a Pydantic model which provides data validation, serialization, and deserialization
        for user entities. This model is typically used in scenarios where user data is being manipulated or
        transmitted, such as during registration, authentication, and authorization processes.

        Example:
        Creating a new user instance can be done by providing values for the required fields:
        new_user = User(id=1, email="user@example.com", hashed_password="hashedpassword123", role="admin")
        Pydantic models automatically convert and validate incoming data, raising errors if invalid data is provided
    """
    id: int
    email: str
    hashed_password: str
    role: str
