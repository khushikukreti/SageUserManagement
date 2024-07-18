from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
        Hashes a password using the specified cryptographic hashing algorithm.

        Args:
        password (str): The plain text password to hash.

        Returns:
        str: The hashed password.

        This function takes a plain text password and uses the `pwd_context` to hash it securely.
        The hashing algorithm used is specified in the `pwd_context` configuration. This is crucial
        for storing passwords securely in the database, ensuring that plain text passwords are never
        stored or transmitted.

        Example:
        plain_password = "securePassword123"
        hashed_password = hash_password(plain_password)
        print("Hashed Password:", hashed_password)
        The hashed password can then be stored in the database for future verification.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
        Verifies a plain text password against a hashed password.

        Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

        Returns:
        bool: True if the verification is successful, False otherwise.

        This function takes a plain text password and a hashed password, and uses the `pwd_context`
        to verify if the plain text password, when hashed, matches the hashed password provided.
        This is typically used during user authentication to verify passwords without ever needing
        to store or compare plain text passwords directly.

        Example:
        user_input_password = "securePassword123"
        stored_hashed_password = "hashed_version_of_password"
        is_verified = verify_password(user_input_password, stored_hashed_password)
        print("Password verified:", is_verified)
        This approach enhances security by ensuring that passwords are always handled in a hashed form.
    """
    return pwd_context.verify(plain_password, hashed_password)
