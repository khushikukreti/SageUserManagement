from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
        Data model for creating a new user.

        Attributes:
        email (EmailStr): Email address of the user. It must be a valid email format.
        password (str): Password for the user. This will be hashed before being stored in the database.

        This model is used to validate and transfer user data when a new user is being registered.
        The email is validated to ensure it adheres to proper email format, enhancing data integrity.

        Example:
        To create a new user, instantiate this model with the user's email and password:
        new_user_data = UserCreate(email="newuser@example.com", password="securePassword123")
    """
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """
        Data model for user response.

        Attributes:
        id (int): Unique identifier for the user, typically the primary key in the database.
        email (EmailStr): Email address of the user. It must be a valid email format.
        role (str): The role assigned to the user within the application, such as 'admin' or 'user'.

        This model is used to provide a structured response after user-related operations, such as
        registration or querying user details. It ensures consistent data format and type safety
        across responses.

        Example:
        To represent a user in API responses, instantiate this model with the user's id, email, and role:
        user_response = UserResponse(id=1, email="user@example.com", role="admin")
    """
    id: int
    email: EmailStr
    role: str
